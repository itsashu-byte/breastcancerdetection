from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile, Prediction

# ==========================================
# LOAD AI MODEL
# ==========================================

try:
    from .ai_model import predict_mammogram
    AI_AVAILABLE = True
    print("AI MODEL IMPORTED SUCCESSFULLY")
except Exception as e:
    AI_AVAILABLE = False
    print("AI MODEL ERROR:", e)


# ==========================================
# HOME
# ==========================================

def index(request):
    return render(request, "index.html")


# ==========================================
# REGISTER
# ==========================================

def register_view(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        age = request.POST.get("age")
        gender = request.POST.get("gender")
        dob = request.POST.get("dob")
        phone = request.POST.get("phone")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        profile_pic = request.FILES.get("profile_pic")

        if password != confirm_password:
            messages.error(
                request,
                "Passwords do not match."
            )
            return redirect("register")

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect("register")

        if User.objects.filter(
            email=email
        ).exists():

            messages.error(
                request,
                "Email already exists."
            )

            return redirect("register")

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        UserProfile.objects.create(
            user=user,
            age=age,
            gender=gender,
            date_of_birth=dob,
            phone_no=phone,
            profile_pic=profile_pic
        )

        messages.success(
            request,
            "Account created successfully."
        )

        return redirect("login")

    return render(
        request,
        "register.html"
    )


# ==========================================
# LOGIN
# ==========================================

def login_view(request):

    if request.method == "POST":

        username = request.POST.get(
            "username"
        )

        password = request.POST.get(
            "password"
        )

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:

            login(
                request,
                user
            )

            return redirect(
                "dashboard"
            )

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(
        request,
        "login.html"
    )


# ==========================================
# LOGOUT
# ==========================================

def logout_view(request):

    logout(request)

    return redirect(
        "home"
    )


# ==========================================
# DASHBOARD
# ==========================================

@login_required
def dashboard_view(request):

    user_profile, created = UserProfile.objects.get_or_create(
        user=request.user
    )

    predictions = Prediction.objects.filter(
        user=request.user
    ).order_by(
        "-created_at"
    )

    total = predictions.count()

    benign = predictions.filter(
        result="Benign"
    ).count()

    malignant = predictions.filter(
        result="Malignant"
    ).count()

    return render(
        request,
        "dashboard.html",
        {
            "user_profile": user_profile,
            "predictions": predictions,
            "total": total,
            "benign": benign,
            "malignant": malignant,
        }
    )


# ==========================================
# UPLOAD + AI PREDICTION
# ==========================================

@login_required
def upload_mammogram(request):

    if request.method == "POST":

        image = request.FILES.get(
            "mammogram_image"
        )

        symptoms = request.POST.getlist(
            "symptoms"
        )

        if not image:

            messages.error(
                request,
                "Please upload a mammogram image."
            )

            return redirect(
                "dashboard"
            )

        symptoms_str = ", ".join(
            symptoms
        ) if symptoms else "None"

        prediction = Prediction.objects.create(
            user=request.user,
            image=image,
            symptoms=symptoms_str,
            result="Processing",
            confidence=0
        )

        try:

            if AI_AVAILABLE:

                result, confidence = predict_mammogram(
                    prediction.image.path
                )

            else:

                result = "Model Error"
                confidence = 0

            prediction.result = result
            prediction.confidence = confidence

            prediction.save()

            messages.success(
                request,
                f"Prediction Completed: {result}"
            )

        except Exception as e:

            print(
                "AI ERROR:",
                str(e)
            )

            prediction.result = "Error"
            prediction.confidence = 0

            prediction.save()

            messages.error(
                request,
                f"Prediction Failed: {str(e)}"
            )

        return redirect(
            "dashboard"
        )

    return redirect(
        "dashboard"
    )