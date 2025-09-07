# loreh/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("load-subservices/", views.load_subservices, name="load_subservices"),
    path("verify-payment/<int:appointment_id>/", views.verify_payment, name="verify_payment"),
]
