import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Avg
from accounts.models import DoctorProfile, User
from appointments.models import Appointment
from .models import Review


def add_review(request, doctor_id):
    if request.session.get("role") != "patient":
        if request.headers.get("x-requested-with"):
            return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)
        return redirect("login")

    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    has_completed = Appointment.objects.filter(
        doctor=doctor,
        patient_id=request.session["user_id"],
        status="completed"
    ).exists()

    if not has_completed:
        msg = "You can only review after a completed appointment."
        if request.headers.get("x-requested-with"):
            return JsonResponse({"success": False, "message": msg})
        return redirect("appointments:my")

    if request.method == "POST":
        rating = 0
        comment = ""

        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
                rating = int(data.get("rating", 0) or 0)
                comment = data.get("text", "")
            except (ValueError, json.JSONDecodeError):
                return JsonResponse({"success": False, "message": "Invalid JSON data"}, status=400)
        else:
            rating = int(request.POST.get("rating", 0) or 0)
            comment = request.POST.get("comment", "")

        if rating < 1 or rating > 5:
            msg = "Invalid rating (1–5 only)."
            if request.headers.get("x-requested-with"):
                return JsonResponse({"success": False, "message": msg})
            return redirect("add_review", doctor_id=doctor.id)

        review, created = Review.objects.update_or_create(
            patient_id=request.session["user_id"],
            doctor=doctor,
            defaults={"rating": rating, "comment": comment},
        )

        if request.headers.get("x-requested-with"):
            return JsonResponse({"success": True, "message": "Review submitted successfully!"})

        messages.success(request, "Review added." if created else "Review updated.")
        return redirect("appointments:my")

    return render(request, "reviews/add_review.html", {"doctor": doctor})


def doctor_reviews(request):
    if request.session.get("role") != "doctor":
        return redirect("login")

    doctor = get_object_or_404(User, id=request.session["user_id"]).doctor_profile
    reviews = doctor.reviews.all().order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    return render(request, "reviews/doctor_reviews.html", {
        "doctor": doctor,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
    })


def doctor_reviews_api(request):
    if request.session.get("role") != "doctor":
        return JsonResponse({"error": "Unauthorized"}, status=403)

    reviews = Review.objects.filter(doctor__user_id=request.session["user_id"]).values(
        "patient__full_name", "rating", "comment", "created_at"
    )

    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    return JsonResponse({
        "avg_rating": round(avg_rating, 1),
        "reviews": list(reviews)
    })