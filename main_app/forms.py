# main_app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'contact_number', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_approved = False  # Set to False until admin approval
        if commit:
            user.save()
        return user
