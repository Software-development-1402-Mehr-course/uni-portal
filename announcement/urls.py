from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("send_private_message", views.send_private_message),
    path("submit_private_message", views.submit_private_message),
    path("submit_announcement", views.submit_announcement),
    path("main", views.main_page)
    # path("inbox", views.inbox),
    # path("user_inbox", views.user_inbox),
]
