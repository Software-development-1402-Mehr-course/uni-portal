from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = "user/login.html"

    def post(self, request):
        user = authenticate(
            username=request.POST["username"], password=request.POST["password"]
        )
        if user:
            login(request, user)
            return redirect("check_user")

        messages.error(request, "Wrong username or password")
        return self.get(self, request)

def logout_view(request):
    logout(request)
    return redirect("check_user")