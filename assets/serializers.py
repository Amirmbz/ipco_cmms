from rest_framework import serializers
from .models import AssetCategory, Asset, AssetAttachment, AssetSparePartLink


class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = '__all__'


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = '__all__'


class AssetAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetAttachment
        fields = '__all__'


class AssetSparePartLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetSparePartLink
        fields = '__all__'