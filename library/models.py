from datetime import datetime, timedelta

from django.db import models

from user.models import Student


class SubjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("name")


class Subject(models.Model):
    objects = SubjectManager()

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AuthorManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("name")


class Author(models.Model):
    objects = AuthorManager()

    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    objects: models.Manager
    booklog_set: models.Manager

    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)
    description = models.TextField(null=True)
    publish_date = models.DateField()
    subjects = models.ManyToManyField(Subject)

    reserved_by = models.ForeignKey(
        Student,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reserved_book",
    )
    taken_by = models.ForeignKey(
        Student,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="taken_book",
    )

    return_due = models.DateField(null=True, blank=True)

    def reserve(self, student_id: int):
        self.reserved_by_id = student_id
        self.save()

        self.booklog_set.create(
            book=self, log_type=BookLog.LogType.RESERVED, student_id=student_id
        )

    def take(self, student_id: int, remove_reservation: bool = False):
        if remove_reservation:
            self.reserved_by_id = None
        self.taken_by_id = student_id
        self.return_due = datetime.now() + timedelta(days=14)
        self.save()

        self.booklog_set.create(
            book=self, log_type=BookLog.LogType.TAKEN, student_id=student_id
        )

    def extend(self, student_id: int):
        self.return_due = datetime.now() + timedelta(days=28)
        self.save()
        self.booklog_set.create(
            book=self, log_type=BookLog.LogType.EXTENDED, student_id=student_id
        )

    def return_back(self):
        self.taken_by_id = None
        self.save()

        self.booklog_set.create(book=self, log_type=BookLog.LogType.RETURNED)

    def availability(self) -> str:
        if self.reserved_by:
            return "Reserved"

        if self.taken_by:
            return "Taken"

        return "Available"

    @property
    def current_fine(self):
        now = datetime.now().date()
        if now > self.return_due:
            return (now - self.return_due).days
        return 0

    def authors_string(self) -> str:
        return " & ".join(author.name for author in self.authors.all())

    def __str__(self):
        return super().__str__() + f" : {self.name}"


class BookLog(models.Model):
    class LogType(models.IntegerChoices):
        RETURNED = 1
        TAKEN = 2
        RESERVED = 3
        EXTENDED = 4

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    log_type = models.PositiveSmallIntegerField(choices=LogType.choices)
    student = models.ForeignKey(Student, null=True, on_delete=models.DO_NOTHING)
    timestamp = models.DateTimeField(auto_now=True)
