# Generated by Django 5.0.1 on 2024-01-25 09:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("course", "0002_coursesubject_alter_course_subject_enrolment_pick_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="CourseSession",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("holds_even_weeks", models.BooleanField(default=True)),
                ("holds_odd_weeks", models.BooleanField(default=True)),
                (
                    "weekday",
                    models.IntegerField(
                        choices=[
                            (1, "Monday"),
                            (2, "Tuesday"),
                            (3, "Wednesday"),
                            (4, "Thursday"),
                            (5, "Friday"),
                            (6, "Saturday"),
                            (7, "Sunday"),
                        ]
                    ),
                ),
                (
                    "course",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="course.course"
                    ),
                ),
            ],
        ),
    ]