from rest_framework import serializers
from .models import (
    PMTemplate,
    PMSchedule,
    ChecklistTemplate,
    ChecklistItemTemplate,
    ChecklistExecution,
    ChecklistItemExecution,
)


class PMTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMTemplate
        fields = '__all__'


class PMScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = PMSchedule
        fields = '__all__'


class ChecklistItemTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItemTemplate
        fields = '__all__'


class ChecklistTemplateSerializer(serializers.ModelSerializer):
    items = ChecklistItemTemplateSerializer(many=True, read_only=True)

    class Meta:
        model = ChecklistTemplate
        fields = '__all__'


class ChecklistExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistExecution
        fields = '__all__'


class ChecklistItemExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItemExecution
        fields = '__all__'