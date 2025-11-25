from rest_framework import serializers
from .models import (
    WorkOrderGroup,
    WorkOrder,
    WorkOrderFailure,
    WorkOrderAction,
    WorkOrderPartUsage,
    WorkOrderAttachment,
    WorkOrderComment,
)


class WorkOrderGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderGroup
        fields = '__all__'


class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'


class WorkOrderFailureSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderFailure
        fields = '__all__'


class WorkOrderActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAction
        fields = '__all__'


class WorkOrderPartUsageSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderPartUsage
        fields = '__all__'


class WorkOrderAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderAttachment
        fields = '__all__'


class WorkOrderCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrderComment
        fields = '__all__'