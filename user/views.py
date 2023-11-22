from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "user/login.html"

    def post(self, request):
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )

        if user is None:
            messages.error(request, "Invalid username or password")
            return redirect("login")

        login(request, user)
        return redirect("check_user")
