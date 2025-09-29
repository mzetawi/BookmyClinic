from django.contrib import admin
from django.utils.html import format_html
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient_name",
        "doctor_name",
        "appointment_date",
        "appointment_time",
        "status",
    )
    list_filter = ("status", "appointment_date")
    search_fields = ("patient__full_name", "doctor__user__full_name")
    ordering = ("-appointment_date", "-appointment_time")

    def patient_name(self, obj):
        return obj.patient.full_name
    patient_name.admin_order_field = "patient__full_name"
    patient_name.short_description = "Patient"

    def doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.full_name}"
    doctor_name.admin_order_field = "doctor__user__full_name"
    doctor_name.short_description = "Doctor"