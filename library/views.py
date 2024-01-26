from dataclasses import dataclass
from functools import cache
from typing import Optional

from django.db.models import Q, QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.base import TemplateView

from common.htmx import HTMXHeaders

from .forms import BookSearchForm
from .models import Book


class BookListView(TemplateView):
    template_name = "library/books.html"
    page_size = 15

    @dataclass
    class QueryParams:
        search_phrase: Optional[str] = None

    @property
    @cache
    def search_form(self):
        form = BookSearchForm(self.request.GET)
        form.is_valid()

        return form

    def search_filter(self) -> Q:
        data = self.search_form.cleaned_data
        filter = Q()

        if search_phrase := data.get("search_phrase"):
            for word in search_phrase.split():
                filter &= Q(name__icontains=word) | Q(authors__name__icontains=word)

        if name := data.get("name"):
            filter &= Q(name__icontains=name)

        if authors := data.get("authors"):
            authors_filter = Q()
            for author_name in authors.split(","):
                authors_filter |= Q(authors__name=author_name.strip())
            filter &= authors_filter

        if publish_year_from := data.get("publish_year_from"):
            filter &= Q(publish_date__year__gte=publish_year_from)

        if publish_year_to := data.get("publish_year_to"):
            filter &= Q(publish_date__year__lte=publish_year_to)

        if subjects := data.get("subjects"):
            filter &= Q(subjects__in=subjects)

        return filter

    def get_books_query(self) -> QuerySet:
        books_query = Book.objects.all()

        books_query = books_query.filter(self.search_filter()).distinct()

        return books_query

    def rest_of_results_count(self) -> int:
        return max(0, self.get_books_query().count() - self.page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.search_form
        context["books"] = self.get_books_query()[: self.page_size]
        context["rest_of_results_count"] = self.rest_of_results_count()
        context["author_names"] = self.search_form.author_names()

        if HTMXHeaders.from_request(self.request) is not None:
            context["base"] = "content.html"

        return context


class BookDetailView(TemplateView):
    template_name = "library/book_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["book"] = Book.objects.get(id=kwargs["book_id"])
        return context


class BookReserveView(View):
    def post(self, request, book_id: int):
        if not request.user.is_authenticated:
            return HttpResponse(
                '<div class="alert alert-danger"> You are not logged in! </div>'
            )
        book: Book = Book.objects.get(id=book_id)
        if book.reserved_by and book.reserved_by.id == request.user.id:
            return HttpResponse(
                '<div class="alert alert-danger"> You have already reserved this book! </div>'
            )

        book.reserve(request.user.id)
        return HttpResponse(
            '<div class="alert alert-success"> Book reserved successfully! </div>'
        )


class BookTakeView(View):
    def post(self, request, book_id: int):
        book: Book = Book.objects.get(id=book_id)
        if not request.user.is_authenticated:
            return HttpResponse(
                '<div class="alert alert-danger"> You are not logged in! </div>'
            )
        user_id = request.user.id
        book.take(user_id)
        return HttpResponse(
            '<div class="alert alert-success"> Book borrowed successfully! </div>'
        )


class BookExtendView(View):
    def post(self, request, book_id: int):
        book: Book = Book.objects.get(id=book_id)
        if not request.user.is_authenticated:
            return HttpResponse(
                '<div class="alert alert-danger"> You are not logged in! </div>'
            )
        if request.user.id == book.taken_by.id:
            user_id = request.user.id
            book.extend(user_id)
            return HttpResponse(
                '<div class="alert alert-success"> Book return time extended successfully! </div>'
            )
        else:
            return redirect("book_detail", book_id=book_id)


class BookReturnView(View):
    def post(self, request, book_id: int):
        book: Book = Book.objects.get(id=book_id)
        if request.user.id == book.taken_by.id:
            book.return_back()
            return HttpResponse('<div class="alert alert-success"> Thank you! </div>')
        else:
            return redirect("book_detail", book_id=book_id)
