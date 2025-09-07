from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["name", "email", "phone", "service", "subservice", "date", "time", "notes"]  # ✅ Added subservice
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "service": forms.Select(attrs={"class": "form-select"}),
            "subservice": forms.Select(attrs={"class": "form-select"}),  # ✅ Added dropdown
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "time": forms.TimeInput(attrs={"type": "time", "class": "form-control"}),
            "notes": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
        }



class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20, required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={"rows": 4}))
