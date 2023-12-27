"""
URL configuration for uni_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import HttpResponse
from django.urls import path

from library.views import BookDetailView, BookListView, BookReserveView
from user.views import LoginView, logout_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", logout_view),
    path("check_user/", lambda request: HttpResponse(request.user), name="check_user"),
    path("library/", BookListView.as_view(), name="book_list"),
    path("library/<int:book_id>", BookDetailView.as_view(), name="book_detail"),
    path(
        "library/reserve/<int:book_id>/", BookReserveView.as_view(), name="book_reserve"
    ),
]
