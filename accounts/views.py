from decimal import Decimal, InvalidOperation
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import User, DoctorProfile
from django.db.models import Avg
from reviews.models import Review

def register_patient(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        full_name = request.POST["full_name"]

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("accounts:register_patient")

        user = User.objects.create_user(
            email=email, password=password, full_name=full_name, role="patient"
        )
        request.session["user_id"] = user.id
        request.session["role"] = user.role
        return redirect("accounts:patient_home")

    return render(request, "accounts/register_patient.html")


def register_doctor(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        full_name = request.POST["full_name"]
        specialty = request.POST["specialty"]
        clinic_location = request.POST["clinic_location"]

        fee = request.POST.get("consultation_fee")
        try:
            fee = Decimal(fee)
        except (InvalidOperation, TypeError):
            messages.error(request, "Please enter a valid consultation fee")
            return redirect("accounts:register_doctor")

        certificate = request.FILES.get("certificate")
        id_card = request.FILES.get("id_card")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect("accounts:register_doctor")

        user = User.objects.create_doctor(
            email=email, password=password, full_name=full_name
        )

        DoctorProfile.objects.create(
            user=user,
            specialty=specialty,
            clinic_location=clinic_location,
            consultation_fee=fee,
            is_approved=True,
            certificate=certificate,
            id_card=id_card,
        )

        request.session["user_id"] = user.id
        request.session["role"] = user.role
        return redirect("accounts:doctor_dashboard")

    return render(request, "accounts/register_doctor.html")


def user_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                request.session["user_id"] = user.id
                request.session["role"] = user.role

                if user.role == "patient":
                    return redirect("accounts:patient_home")

                if user.role == "doctor":
                    if hasattr(user, "doctor_profile") and not user.doctor_profile.is_approved:
                        messages.error(request, "Your account is pending admin approval.")
                        return redirect("accounts:login")
                    return redirect("accounts:doctor_dashboard")
            else:
                messages.error(request, "Wrong password")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "accounts/login.html")


def user_logout(request):
    request.session.flush()
    return redirect("accounts:login")


def patient_home(request):
    if "user_id" not in request.session or request.session.get("role") != "patient":
        return redirect("accounts:login")

    doctors = DoctorProfile.objects.all()
    return render(request, "accounts/patient_home.html", {"doctors": doctors})


def doctor_dashboard(request):
    if "user_id" not in request.session:
        return redirect("accounts:login")

    user = User.objects.get(id=request.session["user_id"])
    if user.role != "doctor":
        return redirect("accounts:login")

    doctor = user.doctor_profile
    if not doctor.is_approved:
        messages.error(request, "Your account is waiting for admin approval.")
        return redirect("accounts:login")

    return render(request, "accounts/doctor_dashboard.html")


def doctor_details(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)

    reviews = Review.objects.filter(doctor=doctor).select_related("patient").order_by("-created_at")
    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"] or 0

    return render(request, "accounts/doctor_details.html", {
        "doctor": doctor,
        "reviews": reviews,
        "avg_rating": round(avg_rating, 1),
    })


def search_doctors(request):
    if not request.session.get("user_id"):
        return JsonResponse({"error": "Unauthorized"}, status=403)

    name = request.GET.get("name", "").strip()
    location = request.GET.get("location", "").strip()
    specialty = request.GET.get("specialty", "").strip()

    doctors = DoctorProfile.objects.all()
    if name:
        doctors = doctors.filter(user__full_name__icontains=name)
    if location:
        doctors = doctors.filter(clinic_location__icontains=location)
    if specialty:
        doctors = doctors.filter(specialty__icontains=specialty)

    data = [
        {
            "id": doc.id,
            "name": doc.user.full_name,
            "specialty": doc.specialty,
            "location": doc.clinic_location,
            "fee": str(doc.consultation_fee),
        }
        for doc in doctors
    ]

    return JsonResponse({"doctors": data})


def doctor_profile(request):
    if "user_id" not in request.session or request.session.get("role") != "doctor":
        return redirect("accounts:login")

    doctor = get_object_or_404(DoctorProfile, user_id=request.session["user_id"])
    return render(request, "accounts/doctor_profile.html", {"doctor": doctor})


@csrf_exempt
def update_doctor_profile(request):
    if "user_id" not in request.session or request.session.get("role") != "doctor":
        return JsonResponse({"success": False, "message": "Unauthorized"}, status=403)

    if request.method == "POST":
        doctor = get_object_or_404(DoctorProfile, user_id=request.session["user_id"])
        doctor.specialty = request.POST.get("specialty")
        doctor.clinic_location = request.POST.get("clinic_location")

        fee = request.POST.get("consultation_fee")
        if fee:
            try:
                doctor.consultation_fee = Decimal(fee)
            except InvalidOperation:
                return JsonResponse(
                    {"success": False, "message": "Invalid consultation fee"},
                    status=400,
                )

        if request.FILES.get("certificate"):
            doctor.certificate = request.FILES["certificate"]
        if request.FILES.get("id_card"):
            doctor.id_card = request.FILES["id_card"]

        doctor.save()

        return JsonResponse(
            {
                "success": True,
                "message": "Profile updated successfully",
                "doctor": {
                    "specialty": doctor.specialty,
                    "clinic_location": doctor.clinic_location,
                    "consultation_fee": str(doctor.consultation_fee),
                },
            }
        )

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)


def register_choice(request):
    return render(request, "accounts/register_choice.html")
