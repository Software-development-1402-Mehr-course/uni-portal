from course.models import Course

from .base_validator import BaseValidator
from .error import ListLevelError


class MaxCreditValidator(BaseValidator):
    def __init__(self, max_credit_sum: int) -> None:
        self.max_credit_sum = max_credit_sum
        self.credit_sum = 0

    def add_course(self, course: Course) -> None:
        self.credit_sum += course.subject.credit

    def remove_course(self, course: Course) -> None:
        self.credit_sum -= course.subject.credit

    def is_valid(self) -> bool:
        return self.credit_sum <= self.max_credit_sum

    def errors(self):
        errs = []

        if self.max_credit_sum < self.credit_sum:
            errs.append(ListLevelError("Sum of chosen course credits is too high."))

        return errs
