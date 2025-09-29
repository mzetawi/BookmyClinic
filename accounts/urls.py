from django.urls import path
from . import views
from reviews import views as review_views

app_name = "accounts"

urlpatterns = [
    path("register/choice/", views.register_choice, name="register_choice"),
    path("register/patient/", views.register_patient, name="register_patient"),
    path("register/doctor/", views.register_doctor, name="register_doctor"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),

    path("patient/home/", views.patient_home, name="patient_home"),

    path("doctor/home/", views.doctor_dashboard, name="doctor_dashboard"),
    path("doctor/<int:doctor_id>/", views.doctor_details, name="doctor_details"),
    path("doctor/profile/", views.doctor_profile, name="doctor_profile"),
    path("doctor/profile/update/", views.update_doctor_profile, name="update_doctor_profile"),

    path("search/", views.search_doctors, name="search_doctors"),

    path("doctor/reviews/", review_views.doctor_reviews, name="doctor_reviews"),
    path("doctor/reviews/api/", review_views.doctor_reviews_api, name="doctor_reviews_api"),
]