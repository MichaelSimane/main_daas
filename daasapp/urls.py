from django.urls import path
from . import views

urlpatterns = [
    path("Homepage", views.Homepage, name="index"),
    path("generate", views.generate, name="generate"),
    path("chat", views.chat, name="chat"),
    path("<int:sowing>/report", views.report, name="report"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("contact", views.contact, name="contact"),
]