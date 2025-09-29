from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils import timezone
from accounts.models import DoctorProfile
from .models import Appointment
from datetime import datetime


def book_appointment(request, doctor_id):
    if "user_id" not in request.session:
        return redirect("login")

    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    if request.method == "POST":
        date_str = request.POST.get("appointment_date")
        time_str = request.POST.get("appointment_time")
        reason = request.POST.get("reason")

        try:
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            time = datetime.strptime(time_str, "%H:%M:%S").time()
        except Exception:
            return JsonResponse({"success": False, "message": "Invalid date or time format"}, status=400)

        appointment_dt = datetime.combine(date, time)
        if timezone.is_naive(appointment_dt):
            appointment_dt = timezone.make_aware(appointment_dt)

        if appointment_dt < timezone.now():
            return JsonResponse({"success": False, "message": "You cannot book in the past"}, status=400)

        Appointment.objects.create(
            patient_id=request.session["user_id"],
            doctor=doctor,
            appointment_date=date,
            appointment_time=time,
            reason=reason,
            status="pending"
        )

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True, "message": "Appointment booked successfully"})

        return redirect("appointments:my")

    return render(request, "appointments/book_appointment.html", {"doctor": doctor})


def my_appointments(request):
    if "user_id" not in request.session:
        return redirect("login")

    appointments = Appointment.objects.filter(
        patient_id=request.session["user_id"]
    ).order_by("-appointment_date", "-appointment_time")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = [
            {
                "doctor": a.doctor.user.full_name,
                "doctor_id": a.doctor.id,
                "date": a.appointment_date.strftime("%Y-%m-%d"),
                "time": a.appointment_time.strftime("%H:%M"),
                "status": a.status,
                "reason": a.reason or ""
            }
            for a in appointments
        ]
        return JsonResponse({"appointments": data})

    return render(request, "appointments/my_appointments.html")


def doctor_appointments(request):
    if "user_id" not in request.session or request.session.get("role") != "doctor":
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": "Unauthorized"}, status=403)
        return redirect("login")

    doctor_profile = get_object_or_404(DoctorProfile, user_id=request.session["user_id"])
    appointments = Appointment.objects.filter(
        doctor=doctor_profile
    ).order_by("-appointment_date", "-appointment_time")

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        data = [
            {
                "id": a.id,
                "patient": a.patient.full_name,
                "date": a.appointment_date.strftime("%Y-%m-%d"),
                "time": a.appointment_time.strftime("%H:%M"),
                "status": a.status,
                "reason": a.reason or ""  
            }
            for a in appointments
        ]
        return JsonResponse({"appointments": data})

    return render(request, "appointments/doctor_appointments.html", {"appointments": appointments})

def update_appointment_status(request, appointment_id, status):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    if "user_id" not in request.session or request.session.get("role") != "doctor":
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)

    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor__user_id=request.session["user_id"]
    )

    if status not in dict(Appointment.STATUS_CHOICES):
        return JsonResponse({"success": False, "message": "Invalid status"}, status=400)

    if status not in ["confirmed", "cancelled"]:
        return JsonResponse({"success": False, "message": "Not allowed"}, status=400)

    appointment.status = status
    appointment.save()

    return JsonResponse({
        "success": True,
        "status": status,
        "message": f"Appointment {status}",
        "id": appointment.id
    })


def mark_completed(request, appointment_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method"}, status=405)

    if "user_id" not in request.session or request.session.get("role") != "doctor":
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)

    appointment = get_object_or_404(
        Appointment, id=appointment_id, doctor__user_id=request.session["user_id"]
    )
    appointment.status = "completed"
    appointment.save()

    return JsonResponse({
        "success": True,
        "status": "completed",
        "message": "Appointment marked as completed",
        "id": appointment.id
    })