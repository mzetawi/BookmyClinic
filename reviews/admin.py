from django.contrib import admin
from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor_name", "patient_name", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("doctor__user__full_name", "patient__full_name")
    ordering = ("-created_at",)

    def doctor_name(self, obj):
        return f"Dr. {obj.doctor.user.full_name}"
    doctor_name.short_description = "Doctor"

    def patient_name(self, obj):
        return obj.patient.full_name
    patient_name.short_description = "Patient"