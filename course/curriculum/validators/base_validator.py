from abc import ABC, abstractmethod
from itertools import product
from typing import Optional, Self

from course.models import Course
from user.models import Student

from .error import ItemLevelError, ListLevelError, ValidationError


class AbstractValidator(ABC):
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


class BaseValidator(AbstractValidator):
    def __or__(self, other: AbstractValidator) -> AbstractValidator:
        return OrValidator(self, other)

    def __and__(self, other: Self) -> AbstractValidator:
        return AndValidator(self, other)


class AndValidator(BaseValidator):
    def __init__(self, *validators: BaseValidator) -> None:
        super().__init__()
        self.validators = validators

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


class OrValidator(BaseValidator):
    seprator = " & "

    def __init__(self, *validators: BaseValidator) -> None:
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
                return ListLevelError(message=error_message)
            case [item_id]:
                return ItemLevelError(item_id=item_id, message=error_message)
