#
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as _login, logout as _logout
from django.contrib.auth.models import User

#
from .models import Lecture, Course


def home(request):
    if request.user.is_authenticated:
        courses = Course.objects.all()
        context = {
            "courses": courses
        }
        return render(request, "courses/home.html", context)
    else:
        return HttpResponseRedirect("courses/login")


def detail(request, course_id):
    if request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        return render(request, "courses/detail.html", {"course": course})

    else:
        return HttpResponseRedirect('/courses/login')


def rate(request, course_id):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, "courses/detail.html")
        else:
            course = Course.objects.get(id=course_id)
            new_rating = float(request.POST.get('rate'))
            course.average_rating(new_rating)
            return HttpResponseRedirect("/courses/")
    else:
        return HttpResponseRedirect("courses/login")





def register(request):
    if request.method == "GET":
        return render(request, "courses/register.html", {})
    else:
        try:
            first_name = request.POST["firstname"]
            last_name = request.POST["lastname"]
            email = request.POST["email"]
            age = request.POST["age"]
            password = request.POST["password"]
            repeat_password = request.POST["repeat_password"]
        except:
            return render(request, "courses/register.html", {"error_message": "Missed Field"})

        if password != repeat_password:
            return render(request, "courses/register.html", {"error_message": "Password not match."})

    user = User.objects.create_user(username=email, email=email, password=password)
    user.first_name = first_name
    user.last_name = last_name
    user.save()

    lecture_user = Lecture(user=user, age=age)
    lecture_user.save()
    return HttpResponseRedirect('/courses/login/')


def login(request):
    if request.method == "GET":
        return render(request, 'courses/login.html', {})
    else:
        try:
            email = request.POST["email"]
            password = request.POST["password"]
        except:
            return render(request, "courses/login.html", {"error_message": "Missed Field"})

    user = authenticate(username=email, password=password)
    print("USER", email, password)
    if user:
        _login(request, user)
        return HttpResponseRedirect('/courses/')

    else:
        return render(request, "courses/login.html", {"error_message": "Email or password is incorrect."})


def logout(request):
    _logout(request)
    return HttpResponseRedirect("/courses/login")