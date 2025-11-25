from django.urls import path
from . import views

app_name = 'locations'

urlpatterns = [
    path('', views.location_tree, name='location_tree'),
    path('plant/<int:plant_id>/', views.location_tree, name='location_tree_by_plant'),
]