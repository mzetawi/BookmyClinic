from django.urls import path
from . import views

app_name = "appointments"

urlpatterns = [
    path("book/<int:doctor_id>/", views.book_appointment, name="book"),
    path("my/", views.my_appointments, name="my"),
    path("doctor/", views.doctor_appointments, name="doctor"),
    path("update/<int:appointment_id>/<str:status>/", views.update_appointment_status, name="update"),
    path("complete/<int:appointment_id>/", views.mark_completed, name="complete"),
]