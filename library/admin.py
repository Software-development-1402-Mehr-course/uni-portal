from django.contrib import admin
from .models import Book, BookLog

admin.site.register(Book)


@admin.register(BookLog)
class BookLogAdmin(admin.ModelAdmin):
    date_hierarchy = "timestamp"
    list_display = ("student", "book", "log_type")
