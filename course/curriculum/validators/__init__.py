from course.curriculum.validators.error import ListLevelError
from course.models import Course, Enrolment
from user.models import Student

from .base_validator import AbstractValidator
from .credit_range_validator import MaxCreditValidator
from .prerequisites_validator import PrerequisitesValidator


class ValidatorFacade:
    validator: AbstractValidator

    def __init__(self, student: Student) -> None:
        self.student = student
        self.reset_validator()

    def reset_validator(self):
        self.validator = MaxCreditValidator(6) & PrerequisitesValidator(self.student)

    def student_valid_courses(self):
        valid_courses: list[Course] = []
        for course in Course.objects.exclude(enrolment__student=self.student):
            self.validator.add_course(course)
            if all(type(error) == ListLevelError for error in self.validator.errors()):
                valid_courses.append(course)

            self.validator.remove_course(course)

        return valid_courses

    def propose_student_curriculum(self):
        for course in Course.objects.filter(
            enrolment__status=Enrolment.Status.LOCKED,
            enrolment__student=self.student,
        ):
            self.validator.add_course(course)

        new_proposed_courses: list[course] = []
        for course in Course.objects.filter(
            enrolment__student=self.student, enrolment__status=Enrolment.Status.PICKED
        ):
            self.validator.add_course(course)
            if self.validator.is_valid():
                new_proposed_courses.append(course)
            else:
                self.validator.remove_course(course)
        self.reset_validator()
        return new_proposed_courses
