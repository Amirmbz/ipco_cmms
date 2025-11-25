from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile
from plants.models import Plant
from accounts.models import Department, Role


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            'department', 'primary_plant', 'role',
            'is_operator', 'is_technician', 'is_supervisor', 'is_manager', 'is_admin'
        ]