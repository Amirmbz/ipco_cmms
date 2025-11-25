from datetime import timedelta
from django.contrib.auth.models import User
from django.utils import timezone

from work_orders.models import WorkOrder
from .models import PMSchedule, ChecklistExecution, ChecklistTemplate


def run_pm_scheduler():
    created = []
    today = timezone.now().date()
    default_user = User.objects.first()
    for sched in PMSchedule.objects.filter(active=True, next_due_date__isnull=False, next_due_date__lte=today):
        asset = sched.asset
        wo = WorkOrder.objects.create(
            code=f"PM-{sched.id}-{today.strftime('%Y%m%d')}",
            plant=asset.plant,
            asset=asset,
            location=asset.location,
            department=asset.department,
            type='PREVENTIVE',
            status='SUBMITTED',
            priority='MEDIUM',
            title=f"PM for {asset}",
            description=sched.template.description,
            requested_by=default_user,
            created_by=default_user,
            is_pm_generated=True,
        )
        checklist_template = ChecklistTemplate.objects.filter(plant=asset.plant).first()
        if checklist_template and default_user:
            ChecklistExecution.objects.create(
                work_order=wo,
                template=checklist_template,
                performed_by=default_user,
                overall_status='PARTIAL',
            )
        created.append(wo)
        sched.last_done_date = today
        if sched.template.interval_days:
            sched.next_due_date = today + timedelta(days=sched.template.interval_days)
        sched.save()
    return created