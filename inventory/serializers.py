from rest_framework import serializers
from .models import Warehouse, PartCategory, Part, PartStock, PartTransaction


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'


class PartCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PartCategory
        fields = '__all__'


class PartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Part
        fields = '__all__'


class PartStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartStock
        fields = '__all__'


class PartTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PartTransaction
        fields = '__all__'