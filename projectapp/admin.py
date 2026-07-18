from django.contrib import admin
from .models import UserProfile, Prediction


# ==========================================
# USER PROFILE ADMIN
# ==========================================

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'age',
        'gender',
        'phone_no',
        'date_of_birth',
        'created_at'
    )

    search_fields = (
        'user__username',
        'user__email',
        'phone_no'
    )

    list_filter = (
        'gender',
        'created_at'
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 20


# ==========================================
# PREDICTION ADMIN
# ==========================================

@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'result',
        'confidence',
        'created_at'
    )

    search_fields = (
        'user__username',
        'user__email',
        'result',
        'symptoms'
    )

    list_filter = (
        'result',
        'created_at'
    )

    readonly_fields = (
        'created_at',
    )

    ordering = (
        '-created_at',
    )

    list_per_page = 25

    fieldsets = (

        ("Patient Information", {
            "fields": (
                "user",
            )
        }),

        ("Mammogram Analysis", {
            "fields": (
                "image",
                "symptoms",
                "result",
                "confidence",
            )
        }),

        ("System Information", {
            "fields": (
                "created_at",
            )
        }),

    )