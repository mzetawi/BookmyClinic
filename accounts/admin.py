from django.contrib import admin
from django.utils.html import format_html
from .models import User, DoctorProfile


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "email", "role")
    search_fields = ("full_name", "email")
    list_filter = ("role",)


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialty", "clinic_location", "consultation_fee", "is_approved")
    list_filter = ("is_approved", "specialty", "clinic_location")
    search_fields = ("user__full_name", "user__email", "specialty", "clinic_location")

    fieldsets = (
        ("Basic Info", {
            "fields": ("user", "specialty", "clinic_location", "consultation_fee", "is_approved"),
        }),
        ("Documents", {
            "fields": ("certificate", "certificate_preview", "id_card", "id_card_preview"),
        }),
    )

    readonly_fields = ("certificate_preview", "id_card_preview")
    actions = ["approve_doctors"]

    def certificate_preview(self, obj):
        if obj.certificate:
            return format_html(
                '<a href="{}" target="_blank" style="font-weight:bold; color:#0d6efd;">📄 View Certificate</a>',
                obj.certificate.url,
            )
        return format_html('<span style="color: #999;">No certificate uploaded</span>')
    certificate_preview.short_description = "Certificate"

    def id_card_preview(self, obj):
        if obj.id_card:
            return format_html(
                '<img src="{}" width="220" style="border:1px solid #ccc; border-radius:6px; padding:2px;"/>',
                obj.id_card.url,
            )
        return format_html('<span style="color: #999;">No ID uploaded</span>')
    id_card_preview.short_description = "ID Card"
    
    def approve_doctors(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} doctor(s) approved successfully.")
    approve_doctors.short_description = "Approve selected doctors"