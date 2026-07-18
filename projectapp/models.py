from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    age = models.IntegerField()
    gender = models.CharField(max_length=10)

    date_of_birth = models.DateField()

    phone_no = models.CharField(max_length=15)

    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username




class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='mammograms/')
    symptoms = models.TextField(blank=True, null=True)  # store comma-separated symptoms or JSON
    result = models.CharField(max_length=20, blank=True)  # Benign / Malignant
    confidence = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"