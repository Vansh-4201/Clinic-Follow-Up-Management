from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone
import secrets


class Clinic(models.Model):
    name = models.CharField(max_length=255)
    clinic_code = models.CharField(
        max_length=20,
        unique=True,
        editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.clinic_code:
            self.clinic_code = secrets.token_hex(4)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.clinic_code})"


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.clinic.name}"


class FollowUp(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('done', 'Done'),
    )

    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('hi', 'Hindi'),
    )

    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    patient_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    notes = models.TextField(blank=True)

    due_date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='pending'
    )

    public_token = models.CharField(
        max_length=32,
        unique=True,
        editable=False
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.public_token:
            self.public_token = secrets.token_urlsafe(12)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.patient_name} ({self.status})"


class PublicViewLog(models.Model):
    followup = models.ForeignKey(FollowUp, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)
    user_agent = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return f"View of {self.followup.id} at {self.viewed_at}"

