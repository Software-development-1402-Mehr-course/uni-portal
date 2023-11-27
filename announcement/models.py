from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Role(models.TextChoices):
        STAFF = "staff"
        PROFESSOR = "professor"
        STUDENT = "student"

class User(models.Model):
    class Meta:
        abstract = True


    name = models.CharField(max_length=20)
    role = models.CharField(max_length=9, choices=Role.choices)

    def can_send_announcement(self):
        return self.role != Role.STUDENT

    def __str__(self):
        return self.name


class Staff(User):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.STAFF


class Professor(User):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.PROFESSOR


class Course(models.Model):
    subject = models.CharField(max_length=30)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.professor}"


class Student(User):
    courses = models.ManyToManyField(Course)

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = Role.STUDENT


class Message(models.Model):
    class Meta:
        abstract = True

    body = models.CharField(max_length=300)

    sender_type = models.CharField(max_length=9, choices=Role.choices)
    sender_pk = models.PositiveIntegerField()

class PrivateMessage(Message):
    """
    Private messages have an indivisual sender and an indivisual reciever.
    """

    reciever_type = models.CharField(max_length=9, choices=Role.choices)
    reciever_pk = models.PositiveIntegerField()

class Announcement(Message):
    """
    Announcements have an indivisual sender and all of one (or more) specefic course attendees as reciever.
    """

    reciever_group = models.ManyToManyField(Course)
