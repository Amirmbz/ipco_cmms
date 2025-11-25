from django.contrib.auth.models import User
from django.db import models


class WorkOrderGroup(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code


class WorkOrder(models.Model):
    TYPE_CHOICES = [
        ('BREAKDOWN', 'Breakdown'),
        ('CORRECTIVE', 'Corrective'),
        ('PREVENTIVE', 'Preventive'),
        ('PROJECT', 'Project'),
    ]
    STATUS_CHOICES = [
        ('SUBMITTED', 'Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('ASSIGNED', 'Assigned'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CHECKED', 'Checked'),
        ('CLOSED', 'Closed'),
        ('RETURNED', 'Returned'),
        ('REJECTED', 'Rejected'),
    ]
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]

    code = models.CharField(max_length=100, unique=True)
    group = models.ForeignKey(WorkOrderGroup, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    plant = models.ForeignKey('plants.Plant', on_delete=models.CASCADE)
    asset = models.ForeignKey('assets.Asset', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey('locations.Location', on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey('accounts.Department', on_delete=models.SET_NULL, null=True, blank=True)

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='SUBMITTED')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_workorders')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workorders')
    assigned_to = models.ManyToManyField(User, related_name='assigned_workorders', blank=True)

    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    downtime_minutes = models.IntegerField(null=True, blank=True)

    is_pm_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.code


class WorkOrderFailure(models.Model):
    CATEGORY_CHOICES = [
        ('MECHANICAL', 'Mechanical'),
        ('ELECTRICAL', 'Electrical'),
        ('CONTROL', 'Control'),
        ('HYDRAULIC', 'Hydraulic'),
        ('OPERATOR', 'Operator'),
        ('OTHER', 'Other'),
    ]
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='failures')
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    failure_mode = models.CharField(max_length=255)
    root_cause = models.CharField(max_length=255)
    effect = models.TextField(blank=True)

    def __str__(self):
        return f"{self.work_order} - {self.category}"


class WorkOrderAction(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='actions')
    technician = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    labor_hours = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.work_order} - {self.technician}"


class WorkOrderPartUsage(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='part_usages')
    transaction = models.ForeignKey('inventory.PartTransaction', on_delete=models.SET_NULL, null=True, blank=True)
    part = models.ForeignKey('inventory.Part', on_delete=models.CASCADE)
    condition = models.CharField(max_length=20, choices=(('NEW', 'New'), ('USED', 'Used'), ('DAMAGED', 'Damaged')))
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.work_order} - {self.part}"


class WorkOrderAttachment(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='workorder_attachments/')
    description = models.CharField(max_length=255, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description or self.file.name


class WorkOrderComment(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.work_order} - {self.author}"
