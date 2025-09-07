from django.contrib import admin
from .models import Service, SubService, Appointment  # import your models

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "price")  # ✅ only include fields that exist
    list_filter = ("name",)           # filter by service name
    search_fields = ("name",)


@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "price")
    list_filter = ("service",)
    search_fields = ("name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "service", "subservice", "date", "time")
    list_filter = ("service", "date")
    search_fields = ("name", "email", "phone")
