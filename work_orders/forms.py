from django import forms
from django.contrib.auth.models import User

from .models import WorkOrder, WorkOrderAction, WorkOrderFailure, WorkOrderPartUsage


class WorkOrderCreateForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['code', 'plant', 'asset', 'location', 'department', 'type', 'priority', 'title', 'description', 'due_date']


class WorkOrderReviewForm(forms.ModelForm):
    assigned_to = forms.ModelMultipleChoiceField(queryset=User.objects.all(), required=False)

    class Meta:
        model = WorkOrder
        fields = ['status', 'priority', 'assigned_to', 'department', 'due_date']


class WorkOrderActionForm(forms.ModelForm):
    class Meta:
        model = WorkOrderAction
        fields = ['description', 'labor_hours']


class WorkOrderFailureForm(forms.ModelForm):
    class Meta:
        model = WorkOrderFailure
        fields = ['category', 'failure_mode', 'root_cause', 'effect']


class WorkOrderPartUsageForm(forms.ModelForm):
    class Meta:
        model = WorkOrderPartUsage
        fields = ['part', 'condition', 'quantity']