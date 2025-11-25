from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from notifications.utils import notify_users
from .forms import (
    WorkOrderCreateForm,
    WorkOrderReviewForm,
    WorkOrderActionForm,
    WorkOrderFailureForm,
    WorkOrderPartUsageForm,
)
from .models import (
    WorkOrder,
    WorkOrderGroup,
    WorkOrderAction,
    WorkOrderFailure,
    WorkOrderPartUsage,
)
from plants.models import Plant
from accounts.models import Department


def _current_user(request):
    if request.user.is_authenticated:
        return request.user
    return User.objects.first()


def workorder_list(request):
    work_orders = WorkOrder.objects.select_related('plant', 'department')
    plants = Plant.objects.all()
    departments = Department.objects.all()

    plant_id = request.GET.get('plant')
    status_value = request.GET.get('status')
    type_value = request.GET.get('type')
    department_id = request.GET.get('department')

    if plant_id:
        work_orders = work_orders.filter(plant_id=plant_id)
    if status_value:
        work_orders = work_orders.filter(status=status_value)
    if type_value:
        work_orders = work_orders.filter(type=type_value)
    if department_id:
        work_orders = work_orders.filter(department_id=department_id)

    return render(request, 'work_orders/workorder_list.html', {
        'work_orders': work_orders,
        'plants': plants,
        'departments': departments,
    })


def workorder_detail(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    review_form = WorkOrderReviewForm(request.POST or None, instance=work_order)
    action_form = WorkOrderActionForm(request.POST or None)
    failure_form = WorkOrderFailureForm(request.POST or None)
    part_form = WorkOrderPartUsageForm(request.POST or None)

    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'review' and review_form.is_valid():
            work_order = review_form.save()
            messages.success(request, 'Work order updated')
            return redirect('work_orders:workorder_detail', pk=pk)
        if form_type == 'action' and action_form.is_valid():
            act = action_form.save(commit=False)
            act.work_order = work_order
            act.technician = _current_user(request)
            act.save()
            messages.success(request, 'Action added')
            return redirect('work_orders:workorder_detail', pk=pk)
        if form_type == 'failure' and failure_form.is_valid():
            failure = failure_form.save(commit=False)
            failure.work_order = work_order
            failure.save()
            messages.success(request, 'Failure added')
            return redirect('work_orders:workorder_detail', pk=pk)
        if form_type == 'part' and part_form.is_valid():
            part_usage = part_form.save(commit=False)
            part_usage.work_order = work_order
            part_usage.save()
            messages.success(request, 'Part usage logged')
            return redirect('work_orders:workorder_detail', pk=pk)
        if form_type == 'complete':
            work_order.status = 'COMPLETED'
            work_order.completed_at = timezone.now()
            if work_order.started_at:
                delta = work_order.completed_at - work_order.started_at
                work_order.downtime_minutes = int(delta.total_seconds() // 60)
            work_order.save()
            notify_users([work_order.requested_by], 'WORKORDER_COMPLETED', f'{work_order.code} completed', work_order)
            messages.success(request, 'Work order completed')
            return redirect('work_orders:workorder_detail', pk=pk)

    actions = work_order.actions.all()
    failures = work_order.failures.all()
    parts = work_order.part_usages.all()
    comments = work_order.comments.all()

    return render(request, 'work_orders/workorder_detail.html', {
        'work_order': work_order,
        'review_form': review_form,
        'action_form': action_form,
        'failure_form': failure_form,
        'part_form': part_form,
        'actions': actions,
        'failures': failures,
        'parts': parts,
        'comments': comments,
    })


def create_workorder(request):
    if request.method == 'POST':
        form = WorkOrderCreateForm(request.POST)
        if form.is_valid():
            wo = form.save(commit=False)
            user = _current_user(request)
            wo.requested_by = user
            wo.created_by = user
            wo.status = 'SUBMITTED'
            wo.save()
            notify_users([user], 'WORKORDER_CREATED', f'Work order {wo.code} created', wo)
            messages.success(request, 'Work order submitted')
            return redirect('work_orders:workorder_detail', pk=wo.pk)
    else:
        form = WorkOrderCreateForm()
    return render(request, 'work_orders/workorder_create.html', {'form': form})


def review_workorder(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    form = WorkOrderReviewForm(request.POST or None, instance=work_order)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Reviewed and assigned')
        return redirect('work_orders:workorder_detail', pk=pk)
    return render(request, 'work_orders/workorder_review.html', {'form': form, 'work_order': work_order})


def execute_workorder(request, pk):
    work_order = get_object_or_404(WorkOrder, pk=pk)
    action_form = WorkOrderActionForm(request.POST or None)
    if request.method == 'POST' and action_form.is_valid():
        act = action_form.save(commit=False)
        act.work_order = work_order
        act.technician = _current_user(request)
        act.save()
        work_order.status = 'IN_PROGRESS'
        if not work_order.started_at:
            work_order.started_at = timezone.now()
        work_order.save()
        messages.success(request, 'Work order updated')
        return redirect('work_orders:workorder_detail', pk=pk)
    return render(request, 'work_orders/workorder_execute.html', {'work_order': work_order, 'action_form': action_form})
