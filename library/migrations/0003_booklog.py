# Generated by Django 4.2.7 on 2023-11-30 05:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
        ("library", "0002_book_description_alter_book_reserved_by_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookLog",
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
                (
                    "log_type",
                    models.PositiveSmallIntegerField(
                        choices=[(1, "Returned"), (2, "Taken"), (3, "Reserved")]
                    ),
                ),
                ("timestamp", models.DateTimeField(auto_now=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.book"
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        to="user.student",
                    ),
                ),
            ],
        ),
    ]
