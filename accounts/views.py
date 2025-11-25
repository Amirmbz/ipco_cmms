from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User

from .forms import UserCreateForm, UserProfileForm
from .models import Department, Role, UserProfile


@login_required
def create_user(request):
    if request.method == 'POST':
        user_form = UserCreateForm(request.POST)
        profile_form = UserProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'User created successfully')
            return redirect('accounts:create_user')
    else:
        user_form = UserCreateForm()
        profile_form = UserProfileForm()
    return render(request, 'accounts/create_user.html', {'user_form': user_form, 'profile_form': profile_form})


def department_list(request):
    departments = Department.objects.all()
    return render(request, 'accounts/department_list.html', {'departments': departments})