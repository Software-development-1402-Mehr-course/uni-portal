from json import loads

from django.views.generic import TemplateView
from django.views.generic.base import HttpResponse

from course.curriculum.token import StudentToken
from course.curriculum.validators import ValidatorFacade
from course.models import Enrolment
from user.models import Student


class PickView(TemplateView):
    template_name = "course/pick.html"

    def valid_courses(self, validator: ValidatorFacade):
        return validator.student_valid_courses()

    def picked_enrolments(self, student: Student):
        return Enrolment.objects.filter(student=student, status=Enrolment.Status.PICKED)

    def tokens(self, student: Student):
        return StudentToken(student).tokens()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        student = self.request.user.student
        validator = ValidatorFacade(student)
        ctx["picked_enrolment"] = self.picked_enrolments(student)
        ctx["valid_courses"] = self.valid_courses(validator)
        ctx["tokens"] = self.tokens(student)
        return ctx

    def post(self, request):
        Enrolment.objects.filter(
            student=request.user.student, status=Enrolment.Status.PICKED
        ).delete()
        picks = []
        for index, pick in enumerate(loads(request.body)):
            picks.append(
                Enrolment(
                    course_id=pick["id"].split("-")[1],
                    student=request.user.student,
                    status=Enrolment.Status.PICKED,
                    priority=index,
                    tokens=pick["val"],
                )
            )

        Enrolment.objects.bulk_create(picks)

        return HttpResponse()
