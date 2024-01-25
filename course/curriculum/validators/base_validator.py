from abc import ABC, abstractmethod
from itertools import product
from typing import Optional

from _typeshed import Self

from course.models import Course
from user.models import Student

from .error import ItemLevelError, UserLevelError, ValidationError


class AbstractValidator(ABC):
    @abstractmethod
    def set_student(self, student: Student) -> None:
        ...

    @abstractmethod
    def add_course(self, course: Course) -> None:
        ...

    @abstractmethod
    def remove_course(self, course: Course) -> None:
        ...

    @abstractmethod
    def is_valid(self) -> bool:
        ...

    @abstractmethod
    def errors(self) -> list[ValidationError]:
        ...

    def __or__(self, other: Self):
        return OrValidator(self, other)

    def __add__(self, other: Self):
        return AndValidator(self, other)


class AndValidator(AbstractValidator):
    def __init__(self, *validators: AbstractValidator) -> None:
        super().__init__()
        self.validators = validators

    def set_student(self, student: Student) -> None:
        for validator in self.validators:
            validator.set_student(student)

    def add_course(self, course: Course) -> None:
        for validator in self.validators:
            validator.add_course(course)

    def remove_course(self, course: Course) -> None:
        for validator in self.validators:
            validator.add_course(course)

    def is_valid(self) -> bool:
        return all(validator.is_valid() for validator in self.validators)

    def errors(self):
        return sum((validator.errors() for validator in self.validators), [])


class OrValidator(AbstractValidator):
    seprator = " & "

    def __init__(self, *validators: AbstractValidator) -> None:
        super().__init__()
        self.validators = validators

    def set_student(self, student: Student) -> None:
        for validator in self.validators:
            validator.set_student(student)

    def add_course(self, course: Course) -> None:
        for validator in self.validators:
            validator.add_course(course)

    def remove_course(self, course: Course) -> None:
        for validator in self.validators:
            validator.add_course(course)

    def is_valid(self) -> bool:
        return not self.errors()

    def errors(self):
        error_chains = product(*[validator.errors() for validator in self.validators])
        error_iterator = map(self.reduce_error_chain, error_chains)
        return [error for error in error_iterator if error]

    def reduce_error_chain(
        self, chain: tuple[ValidationError]
    ) -> Optional[ValidationError]:
        error_item_ids = {
            error.item_id for error in chain if type(error) == ItemLevelError
        }

        error_message = self.seprator.join(error.message for error in chain)
        match list(error_item_ids):
            case []:
                return UserLevelError(message=error_message)
            case [item_id]:
                return ItemLevelError(item_id=item_id, message=error_message)
