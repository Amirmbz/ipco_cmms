from rest_framework import routers, viewsets

from .models import (
    PMTemplate,
    PMSchedule,
    ChecklistTemplate,
    ChecklistItemTemplate,
    ChecklistExecution,
    ChecklistItemExecution,
)
from .serializers import (
    PMTemplateSerializer,
    PMScheduleSerializer,
    ChecklistTemplateSerializer,
    ChecklistItemTemplateSerializer,
    ChecklistExecutionSerializer,
    ChecklistItemExecutionSerializer,
)


class PMTemplateViewSet(viewsets.ModelViewSet):
    queryset = PMTemplate.objects.all()
    serializer_class = PMTemplateSerializer


class PMScheduleViewSet(viewsets.ModelViewSet):
    queryset = PMSchedule.objects.select_related('asset', 'template').all()
    serializer_class = PMScheduleSerializer


class ChecklistTemplateViewSet(viewsets.ModelViewSet):
    queryset = ChecklistTemplate.objects.all()
    serializer_class = ChecklistTemplateSerializer


class ChecklistItemTemplateViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItemTemplate.objects.all()
    serializer_class = ChecklistItemTemplateSerializer


class ChecklistExecutionViewSet(viewsets.ModelViewSet):
    queryset = ChecklistExecution.objects.all()
    serializer_class = ChecklistExecutionSerializer


class ChecklistItemExecutionViewSet(viewsets.ModelViewSet):
    queryset = ChecklistItemExecution.objects.all()
    serializer_class = ChecklistItemExecutionSerializer


router = routers.DefaultRouter()
router.register(r'pm-templates', PMTemplateViewSet)
router.register(r'pm-schedules', PMScheduleViewSet)
router.register(r'checklists', ChecklistTemplateViewSet)
router.register(r'checklist-items', ChecklistItemTemplateViewSet)
router.register(r'checklist-executions', ChecklistExecutionViewSet)
router.register(r'checklist-item-executions', ChecklistItemExecutionViewSet)

urlpatterns = router.urls