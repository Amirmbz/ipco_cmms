from django.urls import path
from . import views

app_name = 'assets'

urlpatterns = [
    path('', views.asset_list, name='asset_list'),
    path('<int:pk>/', views.asset_detail, name='asset_detail'),
]