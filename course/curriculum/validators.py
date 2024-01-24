from abc import ABC, abstractmethod
from dataclasses import dataclass
from itertools import product
from typing import AbstractSet

from django.db.models.fields import validators
from course.models import Course

from user.models import Student


@dataclass
class UserLevelError:
    message: str


@dataclass
class ItemLevelError:
    item_id: int
    message: str


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
    def errors(self) -> list[UserLevelError | ItemLevelError]:
        ...


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

    def errors(self) -> list[UserLevelError | ItemLevelError]:
        return sum((validator.errors() for validator in self.validators), [])
