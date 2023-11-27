from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import random

# Create your views here.


def index(request):
    users = list(User.objects.all())

    return render(request, "index.html", {"users": users})


def main_page(request):
    _name = request.POST["name"]
    # breakpoint()
    if _name == "":
        return redirect("/phase1")
    user = User.objects.get(name=_name)
    if user == None:
        print("Error: No user with name {}".format(u))
        return redirect("/phase1")
    request.session["user"] = user.name
    context = {}
    if user.role == Role.STUDENT:
        attendances = Attendee.objects.filter(student=user)
        user_courses = [a.course for a in attendances.iterator()]
        announcements = Announcement.objects.filter(reciever_group__in=user_courses)
        context["name"] = user.name
        context["is_student"] = True
        context["announcements"] = announcements
        context["has_announcement"] = len(announcements) > 0
    elif user.role == Role.PROFESSOR:
        teaching = Course.objects.filter(professor=user)
        context["name"] = user.name
        context["is_student"] = False
        context["courses"] = list(teaching)

    else:
        all_course = Course.objects.all()
        context["name"] = user.name
        context["is_student"] = False
        context["courses"] = list(all_course)

    pms = PrivateMessage.objects.filter(receiver=user)
    users = User.objects.all()
    context["pms"] = list(pms)
    context["users"] = list(users)
    context["has_private_message"] = len(pms) > 0

    return render(request, "main.html", context)


def send_private_message(request):
    users = list(User.objects.all())
    users_random_order = random.sample(users, len(users))
    return render(
        request, "send_private_message.html", {"from": users, "to": users_random_order}
    )


def submit_private_message(request):
    _from = request.session["user"]
    _to = request.POST["to"]
    message = request.POST["message"]

    try:
        from_user = User.objects.get(name=_from)
        to_user = User.objects.get(name=_to)
    except:
        return redirect("/phase1")
    # TODO: check users exist

    pm = PrivateMessage(sender=from_user, receiver=to_user, body=message)
    pm.save()

    return HttpResponse("OK!")


def submit_announcement(request):
    _from = request.session["user"]
    _to = request.POST["to"]
    message = request.POST["message"]
    # breakpoint()
    try:
        from_user = User.objects.get(name=_from)
        to_course = Course.objects.get(subject=_to)
    except:
        return redirect("/phase1")
    # TODO: check users exist

    a = Announcement(sender=from_user, body=message, reciever_group=to_course)
    a.save()

    return HttpResponse("OK!")
