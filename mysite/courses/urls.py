from django.urls import path
from . import views

app_name = "courses"

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("<int:course_id>", views.detail, name="detail"),
    path("<int:course_id>/rate/", views.rate, name="rate")
]