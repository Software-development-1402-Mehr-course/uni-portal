from dataclasses import dataclass
from functools import cache
from typing import Optional

from django.db.models import Q, QuerySet
from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.base import TemplateView

from common.htmx import HTMXHeaders

from .models import Book


class BookListView(TemplateView):
    template_name = "library/books.html"

    page_size = 15

    @dataclass
    class QueryParams:
        search_phrase: Optional[str] = None

    @property
    @cache
    def query_params(self):
        return self.QueryParams(**self.request.GET.dict())

    def search_filter(self) -> Q:
        filter = Q()
        if not self.query_params.search_phrase:
            return filter

        for word in self.query_params.search_phrase.split():
            filter &= Q(name__icontains=word) | Q(authors__name__icontains=word)

        return filter

    def get_books_query(self) -> QuerySet:
        books_query = Book.objects.all()

        books_query = books_query.filter(self.search_filter()).distinct()

        return books_query

    def rest_of_results_count(self) -> int:
        return max(0, self.get_books_query().count() - self.page_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query_params"] = self.query_params
        context["books"] = self.get_books_query()[: self.page_size]
        context["rest_of_results_count"] = self.rest_of_results_count()

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
        book: Book = Book.objects.get(id=book_id)
        book.reserve(request.user.id)

        return redirect("book_detail", book_id=book_id)


class BookTakeView(View):
    def post(self, _, student_id: int, book_id: int):
        book: Book = Book.objects.get(id=book_id)
        book.take(student_id)

        return redirect("book_detail", book_id=book_id)


class BookReturnView(View):
    def post(self, _, book_id: int):
        book: Book = Book.objects.get(id=book_id)
        book.return_back()

        return redirect("book_detail", book_id=book_id)
