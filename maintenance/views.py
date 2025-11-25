from django.contrib import messages
from django.shortcuts import render, redirect

from .models import PMTemplate, ChecklistTemplate
from .services import run_pm_scheduler


def pm_template_list(request):
    templates = PMTemplate.objects.all()
    return render(request, 'maintenance/pm_template_list.html', {'templates': templates})


def checklist_template_list(request):
    templates = ChecklistTemplate.objects.all()
    return render(request, 'maintenance/checklist_template_list.html', {'templates': templates})


def run_scheduler_view(request):
    created = []
    if request.method == 'POST':
        created = run_pm_scheduler()
        messages.success(request, f"Scheduler created {len(created)} work orders")
    return render(request, 'maintenance/run_scheduler.html', {'created': created})