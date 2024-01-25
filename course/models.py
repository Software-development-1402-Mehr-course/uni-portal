from django.db import models

from user.models import Professor, Student


class CourseSubject(models.Model):
    prerequisites = models.ManyToManyField("self")
    name = models.TextField(unique=True)
    credit = models.PositiveSmallIntegerField()


class Course(models.Model):
    teacher = models.ForeignKey(Professor, on_delete=models.CASCADE)
    subject = models.ForeignKey(CourseSubject, on_delete=models.PROTECT)
    enrolment_cap = models.PositiveSmallIntegerField()


class CourseSession(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 1
        TUESDAY = 2
        WEDNESDAY = 3
        THURSDAY = 4
        FRIDAY = 5
        SATURDAY = 6
        SUNDAY = 7

    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    holds_even_weeks = models.BooleanField(default=True)
    holds_odd_weeks = models.BooleanField(default=True)
    weekday = models.IntegerField(choices=Weekday)
    time_slot = models.IntegerChoices(
        "TimeSlot",
        "8.AM 10.AM 12.AM 2.PM 4.PM 6.PM",
    )


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
