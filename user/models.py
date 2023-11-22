from django.contrib.auth.models import User


class Student(User):
    class Meta(User.Meta):
        verbose_name = "student"
        verbose_name_plural = "students"


class Professor(User):
    class Meta(User.Meta):
        verbose_name = "professor"
        verbose_name_plural = "professors"


class Staff(User):
    class Meta(User.Meta):
        verbose_name = "staff member"
        verbose_name_plural = "staff"
