from django.urls import path
from . import views

app_name = 'inventory'

urlpatterns = [
    path('warehouses/', views.warehouse_list, name='warehouse_list'),
    path('warehouses/<int:pk>/', views.warehouse_detail, name='warehouse_detail'),
    path('parts/', views.part_list, name='part_list'),
    path('parts/<int:pk>/', views.part_detail, name='part_detail'),
]