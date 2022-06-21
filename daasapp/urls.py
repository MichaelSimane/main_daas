from django.urls import path
from . import views
from urllib import request
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("Homepage", views.Homepage, name="Homepage"),
    path("generate", views.generate, name="generate"),
    path("chat", views.chat, name="chat"),
    path("<str:sowing>/<str:harvesting>/<str:locust>/<str:district>/report", views.report, name="report"),
    path("<int:year>/<int:month><str:district>/<str:sowing>/<str:harvesting>/<str:locust>/detailReport", views.detailReport, name="detailReport"),
    # path("login", views.login, name="login"),
    # path("signup", views.signup, name="signup"),
    path("contact", views.contact, name="contact"),
    path("map", views.map, name="map"),
    path("signup", views.register, name="register"),
    path("login", views.signin, name="signin"),
    path("logout", views.signout, name="signout"),
    path("view_profile", views.view_profile, name="view_profile"),
    
]