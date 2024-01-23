from django.db import models

from user.models import Professor, Student


class Course(models.Model):
    teacher = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.TextField()

