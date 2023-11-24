from django.db import models

from user.models import Professor, Student


class Course(models.Model):
    teacher = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.TextField()


class Attendee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
