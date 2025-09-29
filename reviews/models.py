from django.db import models
from accounts.models import User, DoctorProfile


class ReviewManager(models.Manager):
    def create_review(self, patient, doctor, rating, comment=""):
        review, created = self.update_or_create(
            patient=patient,
            doctor=doctor,
            defaults={"rating": rating, "comment": comment}
        )
        return review, created


class Review(models.Model):
    doctor = models.ForeignKey(
        DoctorProfile, on_delete=models.CASCADE, related_name="reviews"
    )
    patient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reviews"
    )
    rating = models.PositiveSmallIntegerField()  
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ReviewManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "patient"],
                name="unique_doctor_patient_review"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"⭐ {self.rating}/5 by {self.patient.full_name} for Dr. {self.doctor.user.full_name}"