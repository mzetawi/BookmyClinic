from django.db import models
from django.contrib.auth.hashers import make_password, check_password as django_check_password
from django.utils import timezone


class UserManager(models.Manager):
    def create_user(self, email, full_name, password, role="patient"):
        if not email:
            raise ValueError("Email is required")

        email = email.lower().strip()
        user = self.model(
            email=email,
            full_name=full_name,
            password=make_password(password),
            role=role,
        )
        user.save(using=self._db)
        return user

    def create_doctor(self, email, full_name, password):
        return self.create_user(email, full_name, password, role="doctor")

    def create_admin(self, email, full_name, password):
        return self.create_user(email, full_name, password, role="admin")


class User(models.Model):
    ROLE_CHOICES = (
        ("patient", "Patient"),
        ("doctor", "Doctor"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    def __str__(self):
        return self.full_name

    def check_password(self, raw_password):
        return django_check_password(raw_password, self.password)


class DoctorProfile(models.Model):
    SPECIALTY_CHOICES = [
        ("Cardiology", "Cardiology (Heart)"),
        ("Dermatology", "Dermatology (Skin)"),
        ("Pediatrics", "Pediatrics (Children)"),
        ("Neurology", "Neurology"),
        ("General", "General Medicine"),
        ("Dentistry", "Dentistry"),
        ("Orthopedics", "Orthopedics"),
        ("Psychiatry", "Psychiatry"),
        ("ENT", "Ear, Nose & Throat"),
        ("Ophthalmology", "Ophthalmology"),
    ]

    LOCATION_CHOICES = [
        ("Ramallah", "Ramallah"),
        ("Nablus", "Nablus"),
        ("Hebron", "Hebron"),
        ("Jenin", "Jenin"),
        ("Tulkarm", "Tulkarm"),
        ("Jerusalem", "Jerusalem"),
        ("Gaza", "Gaza"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor_profile")
    specialty = models.CharField(max_length=100, choices=SPECIALTY_CHOICES)
    clinic_location = models.CharField(max_length=200, choices=LOCATION_CHOICES)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)
    is_approved = models.BooleanField(default=True)

    certificate = models.FileField(upload_to="certificates/", null=True, blank=True)
    id_card = models.ImageField(upload_to="id_cards/", null=True, blank=True)

    def __str__(self):
        return f"Dr. {self.user.full_name} - {self.specialty}"
