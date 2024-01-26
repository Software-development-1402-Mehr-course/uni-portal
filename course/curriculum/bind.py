from django.db.models import F, Q, Count
from user.models import Student
from course.models import Course, Enrolment
from course.curriculum.validators import ValidatorFacade
from django.db.transaction import atomic


class BindCourses:
    @classmethod
    @atomic
    def bind(cls):
        if not Enrolment.objects.filter(status=Enrolment.Status.PICKED):
            return

        for student in Student.objects.filter(
            enrolment__status=Enrolment.Status.PICKED
        ).distinct():
            proposed_curriculum = ValidatorFacade(student).propose_student_curriculum()
            enrolment_ids = [enrolment.id for enrolment in proposed_curriculum]
            updated_rows = Enrolment.objects.filter(
                status=Enrolment.Status.PICKED, id__in=enrolment_ids
            ).update(status=Enrolment.Status.PROPOSED)

            if not updated_rows:
                Enrolment.objects.filter(status=Enrolment.Status.PICKED).delete()

        enrolment_count = Count(
            "enrolment",
            Q(
                enrolment__status__in=[
                    Enrolment.Status.LOCKED,
                    Enrolment.Status.PROPOSED,
                ]
            ),
        )
        for course in Course.objects.annotate(enrolment_count=enrolment_count).filter(
            enrolment_cap__gt=F("enrolment_count")
        ):
            course_enrolments = Enrolment.objects.filter(course=course)
            locked_in_students = course_enrolments.filter(
                status=Enrolment.Status.LOCKED
            ).count()
            accepted_proposal_ids = (
                course_enrolments.filter(status=Enrolment.Status.PROPOSED)
                .order_by("-tokens")[: course.enrolment_cap - locked_in_students]
                .values_list("id", flat=True)
            )
            Enrolment.objects.filter(id__in=accepted_proposal_ids).update(
                status=Enrolment.Status.LOCKED
            )
            course_enrolments.filter(
                status__in=[Enrolment.Status.PROPOSED, Enrolment.Status.PICKED]
            ).delete()

        Enrolment.objects.filter(status=Enrolment.Status.PROPOSED).update(
            status=Enrolment.Status.LOCKED
        )
