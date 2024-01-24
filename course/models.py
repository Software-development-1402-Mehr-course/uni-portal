from django.db import models

from user.models import Professor, Student

class CourseSubject(models.Model):
    prerequisites = models.ManyToManyField('self')
    subject = models.TextField(unique=True)

class Course(models.Model):
    teacher = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(CourseSubject, on_delete=models.PROTECT)


class Enrolment(models.Model):
    class Status(models.IntegerChoices):
        PICKED = 1
        PROPOSED = 2
        LOCKED = 3
        PASSED = 4
        FAILED = 5

    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.IntegerField(choices=Status)


class Pick(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    priority = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = ["student", "priority"]
