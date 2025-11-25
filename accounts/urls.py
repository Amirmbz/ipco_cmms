from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('users/create/', views.create_user, name='create_user'),
    path('departments/', views.department_list, name='department_list'),
]