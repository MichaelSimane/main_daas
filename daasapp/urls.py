from django.urls import path
from . import views

urlpatterns = [
    path("Homepage", views.Homepage, name="Homepage"),
    path("generate", views.generate, name="generate"),
    path("chat", views.chat, name="chat"),
    path("<str:sowing>/<str:harvesting>/<str:locust>/<str:district>/report", views.report, name="report"),
    path("<int:year>/<int:month><str:district>/<str:sowing>/<str:harvesting>/<str:locust>/detailReport", views.detailReport, name="detailReport"),
    path("login", views.login, name="login"),
    path("signup", views.signup, name="signup"),
    path("contact", views.contact, name="contact"),
    path("map", views.map, name="map"),
]