from django.contrib.auth.models import User
from django.db import models


class Department(models.Model):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.code} - {self.name}"


class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey('Department', on_delete=models.SET_NULL, null=True, blank=True)
    primary_plant = models.ForeignKey('plants.Plant', on_delete=models.SET_NULL, null=True, blank=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True, blank=True)
    is_operator = models.BooleanField(default=False)
    is_technician = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name() or self.user.username