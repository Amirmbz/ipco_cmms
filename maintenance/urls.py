from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('pm-templates/', views.pm_template_list, name='pm_templates'),
    path('checklist-templates/', views.checklist_template_list, name='checklist_templates'),
    path('run-scheduler/', views.run_scheduler_view, name='run_scheduler'),
]