from django.db.models import Subquery

from course.curriculum.validators.error import ItemLevelError
from course.models import Course, CourseSubject, Enrolment
from user.models import Student

from .base_validator import BaseValidator


class PrerequisitesValidator(BaseValidator):
    def __init__(self, student: Student) -> None:
        self.invalid_item_ids: set[int] = set()
        self.student = student

    def add_course(self, course: Course) -> None:
        passed_subjects = CourseSubject.objects.filter(
            course__enrolment__student=self.student,
            course__enrolment__status=Enrolment.Status.PASSED,
        )
        if course.subject.prerequisites.exclude(id__in=passed_subjects):
            self.invalid_item_ids.add(course.id)

    def remove_course(self, course: Course) -> None:
        if course.id in self.invalid_item_ids:
            self.invalid_item_ids.remove(course.id)

    def is_valid(self) -> bool:
        return not self.invalid_item_ids

    def errors(self):
        errs = []

        for invalid_item_id in self.invalid_item_ids:
            message = f"Student hasn't passed {Course.objects.get(id=invalid_item_id).name} prerequisites."
            ItemLevelError(item_id=invalid_item_id, message=message)

        return errs
