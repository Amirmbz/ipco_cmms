from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import routers, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from notifications.utils import notify_users
from .models import (
    WorkOrderGroup,
    WorkOrder,
    WorkOrderFailure,
    WorkOrderAction,
    WorkOrderPartUsage,
    WorkOrderAttachment,
    WorkOrderComment,
)
from .serializers import (
    WorkOrderGroupSerializer,
    WorkOrderSerializer,
    WorkOrderFailureSerializer,
    WorkOrderActionSerializer,
    WorkOrderPartUsageSerializer,
    WorkOrderAttachmentSerializer,
    WorkOrderCommentSerializer,
)


class WorkOrderGroupViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderGroup.objects.all()
    serializer_class = WorkOrderGroupSerializer


class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer

    def _supervisors(self, work_order):
        if not work_order.department:
            return User.objects.none()
        return User.objects.filter(userprofile__department=work_order.department, userprofile__is_supervisor=True)

    def perform_create(self, serializer):
        work_order = serializer.save()
        recipients = [work_order.requested_by, work_order.created_by]
        notify_users(filter(None, recipients), 'WORKORDER_CREATED', f'Work order {work_order.code} created', work_order)
        notify_users(self._supervisors(work_order), 'WORKORDER_CREATED', f'Work order {work_order.code} created', work_order)
        return work_order

    @action(detail=True, methods=['post'])
    def change_status(self, request, pk=None):
        work_order = self.get_object()
        status_value = request.data.get('status')
        if status_value:
            work_order.status = status_value
            work_order.save(update_fields=['status'])
            notify_users([work_order.requested_by], 'WORKORDER_STATUS', f'{work_order.code} status changed to {status_value}', work_order)
            notify_users(work_order.assigned_to.all(), 'WORKORDER_STATUS', f'{work_order.code} status changed to {status_value}', work_order)
        return Response(self.get_serializer(work_order).data)

    @action(detail=True, methods=['post'])
    def assign(self, request, pk=None):
        work_order = self.get_object()
        user_ids = request.data.get('technicians', [])
        qs = User.objects.filter(id__in=user_ids)
        work_order.assigned_to.set(qs)
        work_order.status = 'ASSIGNED'
        work_order.save()
        notify_users(qs, 'WORKORDER_ASSIGNED', f'Assigned to {work_order.code}', work_order)
        notify_users([work_order.requested_by], 'WORKORDER_ASSIGNED', f'{work_order.code} assigned', work_order)
        return Response(self.get_serializer(work_order).data)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        work_order = self.get_object()
        work_order.started_at = timezone.now()
        work_order.status = 'IN_PROGRESS'
        work_order.save(update_fields=['started_at', 'status'])
        notify_users(work_order.assigned_to.all(), 'WORKORDER_STARTED', f'{work_order.code} started', work_order)
        return Response(self.get_serializer(work_order).data)

    @action(detail=True, methods=['post'])
    def finish(self, request, pk=None):
        work_order = self.get_object()
        work_order.completed_at = timezone.now()
        work_order.status = 'COMPLETED'
        if work_order.started_at:
            delta = work_order.completed_at - work_order.started_at
            work_order.downtime_minutes = int(delta.total_seconds() // 60)
        work_order.save(update_fields=['completed_at', 'status', 'downtime_minutes'])
        notify_users([work_order.requested_by], 'WORKORDER_COMPLETED', f'{work_order.code} completed', work_order)
        notify_users(work_order.assigned_to.all(), 'WORKORDER_COMPLETED', f'{work_order.code} completed', work_order)
        return Response(self.get_serializer(work_order).data)


class WorkOrderFailureViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderFailure.objects.all()
    serializer_class = WorkOrderFailureSerializer


class WorkOrderActionViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderAction.objects.all()
    serializer_class = WorkOrderActionSerializer


class WorkOrderPartUsageViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderPartUsage.objects.all()
    serializer_class = WorkOrderPartUsageSerializer


class WorkOrderAttachmentViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderAttachment.objects.all()
    serializer_class = WorkOrderAttachmentSerializer


class WorkOrderCommentViewSet(viewsets.ModelViewSet):
    queryset = WorkOrderComment.objects.all()
    serializer_class = WorkOrderCommentSerializer


router = routers.DefaultRouter()
router.register(r'groups', WorkOrderGroupViewSet)
router.register(r'work-orders', WorkOrderViewSet)
router.register(r'failures', WorkOrderFailureViewSet)
router.register(r'actions', WorkOrderActionViewSet)
router.register(r'part-usages', WorkOrderPartUsageViewSet)
router.register(r'attachments', WorkOrderAttachmentViewSet)
router.register(r'comments', WorkOrderCommentViewSet)

urlpatterns = router.urls
