from django.shortcuts import redirect
from django.views.generic import View
from django.views.generic.base import TemplateView

from .models import Book


class BookListView(TemplateView):
    template_name = "library/books.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books_query = Book.objects.all()

        search_term = self.request.GET.get("q")
        if search_term:
            books_query = books_query.filter(name__icontains=search_term)

        context["books"] = books_query[:10]
        context["search_term"] = search_term
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
