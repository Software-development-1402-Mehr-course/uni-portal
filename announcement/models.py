from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.


class User(models.Model):
    class Meta:
        abstract = True

    class Role(models.TextChoices):
        STAFF = "staff"
        PROFESSOR = "professor"
        STUDENT = "student"

    name = models.CharField(max_length=20)
    role = models.CharField(max_length=9, choices=Role.choices)

    def can_send_announcement(self):
        return self.role != Role.STUDENT

    def __str__(self):
        return self.name


class Staff(User):
    pass


class Professor(User):
    pass


class Course(models.Model):
    subject = models.CharField(max_length=30)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.subject} - {self.professor}"


class Student(User):
    courses = models.ManyToManyField(Course)


class Message(models.Model):
    class Meta:
        abstract = True

    body = models.CharField(max_length=300)
    
    sender_content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE)
    sender_object_id = models.PositiveIntegerField()
    sender_object = GenericForeignKey("sender_content_type","sender_object_id")
    

class PrivateMessage(Message):
    """
    Private messages have an indivisual sender and an indivisual reciever.
    """
    reciever_content_type = models.ForeignKey(ContentType,related_name="reciver_content_type",on_delete=models.CASCADE)
    reciever_object_id = models.PositiveIntegerField()
    reciever_object = GenericForeignKey("reciever_content_type","reciever_object_id")

class Announcement(Message):
    """
    Announcements have an indivisual sender and all of one (or more) specefic course attendees as reciever. 
    """
    reciever_group = models.ManyToManyField(Course)
    
