from django.db import models
from course.models import Course

class AbstractAnnouncement(models.Model):
    message = models.TextField()

    class Meta:
        abstract = True


class GeneralAnnouncement(AbstractAnnouncement):
    pass

class CourseAnnouncement(AbstractAnnouncement):
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING)

