from django.views import TemplateView


class PickView(TemplateView):
    template_name = "course/pick.html"
