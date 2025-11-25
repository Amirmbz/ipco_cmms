from django.contrib.auth.models import User
from django.db import models


class PMTemplate(models.Model):
    FREQUENCY_TYPE_CHOICES = [
        ('DAY_BASED', 'Day Based'),
        ('RUNTIME_BASED', 'Runtime Based'),
    ]

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    asset = models.ForeignKey('assets.Asset', on_delete=models.SET_NULL, null=True, blank=True)
    asset_category = models.ForeignKey('assets.AssetCategory', on_delete=models.SET_NULL, null=True, blank=True)
    frequency_type = models.CharField(max_length=20, choices=FREQUENCY_TYPE_CHOICES)
    interval_days = models.IntegerField(null=True, blank=True)
    interval_hours = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PMSchedule(models.Model):
    template = models.ForeignKey(PMTemplate, on_delete=models.CASCADE)
    asset = models.ForeignKey('assets.Asset', on_delete=models.CASCADE)
    next_due_date = models.DateField(null=True, blank=True)
    last_done_date = models.DateField(null=True, blank=True)
    last_done_hours = models.IntegerField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.asset} - {self.template}"


class ChecklistTemplate(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    asset = models.ForeignKey('assets.Asset', on_delete=models.SET_NULL, null=True, blank=True)
    asset_category = models.ForeignKey('assets.AssetCategory', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class ChecklistItemTemplate(models.Model):
    checklist = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, related_name='items')
    text = models.CharField(max_length=255)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.text


class ChecklistExecution(models.Model):
    OVERALL_STATUS_CHOICES = [
        ('OK', 'OK'),
        ('NOT_OK', 'Not OK'),
        ('PARTIAL', 'Partial'),
    ]

    work_order = models.ForeignKey('work_orders.WorkOrder', on_delete=models.CASCADE, related_name='checklist_executions')
    template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE)
    performed_by = models.ForeignKey(User, on_delete=models.CASCADE)
    performed_at = models.DateTimeField(auto_now_add=True)
    overall_status = models.CharField(max_length=20, choices=OVERALL_STATUS_CHOICES)

    def __str__(self):
        return f"{self.template} - {self.work_order}"


class ChecklistItemExecution(models.Model):
    execution = models.ForeignKey(ChecklistExecution, on_delete=models.CASCADE, related_name='item_executions')
    template_item = models.ForeignKey(ChecklistItemTemplate, on_delete=models.CASCADE)
    is_ok = models.BooleanField(null=True)
    comment = models.TextField(blank=True)

    def __str__(self):
        return f"{self.template_item} - {self.execution}"