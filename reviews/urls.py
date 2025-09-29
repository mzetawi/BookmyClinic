from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:doctor_id>/", views.add_review, name="add_review"),

    path("doctor/reviews/", views.doctor_reviews, name="doctor_reviews"),
    path("doctor/reviews/api/", views.doctor_reviews_api, name="doctor_reviews_api"),
]