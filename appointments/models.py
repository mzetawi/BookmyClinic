from django.db import models
from django.utils import timezone
from accounts.models import User, DoctorProfile


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="appointments"
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "appointment_time"],
                name="unique_doctor_appointment"
            ),
        ]

    def __str__(self):
        return f"{self.patient.full_name} → Dr. {self.doctor.user.full_name} ({self.status})"

    @property
    def is_future(self):
        dt = timezone.datetime.combine(self.appointment_date, self.appointment_time)
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt)
        return dt > timezone.now()