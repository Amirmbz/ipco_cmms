from django.urls import path
from . import views

app_name = 'work_orders'

urlpatterns = [
    path('', views.workorder_list, name='workorder_list'),
    path('create/', views.create_workorder, name='workorder_create'),
    path('<int:pk>/', views.workorder_detail, name='workorder_detail'),
    path('<int:pk>/review/', views.review_workorder, name='workorder_review'),
    path('<int:pk>/execute/', views.execute_workorder, name='workorder_execute'),
]