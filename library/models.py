from django.db import models
from django.utils.translation import gettext

from user.models import Student


class Book(models.Model):
    objects: models.Manager

    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(null=True)

    reserved_by = models.ForeignKey(
        Student, null=True, on_delete=models.SET_NULL, related_name="reserved_book"
    )
    taken_by = models.ForeignKey(
        Student, null=True, on_delete=models.PROTECT, related_name="taken_book"
    )

    def reserve(self, student_id: int):
        self.reserved_by_id = student_id

    def take(self, student_id: int):
        if self.reserved_by_id == student_id:
            self.reserved_by_id = None
        self.taken_by_id = student_id

    def availability(self) -> str:
        if self.reserved_by:
            return gettext("Reserved")

        if self.taken_by:
            return gettext("Taken")

        return gettext("Available")
