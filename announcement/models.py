from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class Role(models.TextChoices):
    STAFF = "staff"
    PROFESSOR = "professor"
    STUDENT = "student"


class User(models.Model):
    name = models.CharField(max_length=20)
    role = models.CharField(max_length=9, choices=Role.choices)

    def can_send_announcement(self):
        return self.role != Role.STUDENT

    def __str__(self):
        return self.name


class Course(models.Model):
    subject = models.CharField(max_length=30)
    professor = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.professor}"


class Attendee(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)


class Message(models.Model):
    class Meta:
        abstract = True

    body = models.CharField(max_length=300)
    datetime = models.DateTimeField(auto_now=True)

    sender = models.ForeignKey(User, on_delete=models.CASCADE)

class PrivateMessage(Message):
    """
    Private messages have an indivisual sender and an indivisual reciever.
    """

    receiver = models.ForeignKey(User, related_name="receiver", on_delete=models.CASCADE)

class Announcement(Message):
    """
    Announcements have an indivisual sender and all of one (or more) specefic course attendees as reciever.
    """

    reciever_group = models.ForeignKey(Course,on_delete=models.CASCADE)
