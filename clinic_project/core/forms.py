from django import forms
from django.utils import timezone
from .models import FollowUp


class FollowUpForm(forms.ModelForm):
    class Meta:
        model = FollowUp
        fields = [
            "patient_name",
            "phone",
            "language",
            "notes",
            "due_date",
        ]
        widgets = {
            "due_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "placeholder": "yyyy-mm-dd",
                }
            )
        }

    def clean_phone(self):
        phone = self.cleaned_data["phone"]
        if not phone.isdigit() or len(phone) < 8:
            raise forms.ValidationError("Enter a valid phone number.")
        return phone

    def clean_due_date(self):
        due_date = self.cleaned_data["due_date"]
        if due_date < timezone.now().date():
            raise forms.ValidationError("Due date cannot be in the past.")
        return due_date
