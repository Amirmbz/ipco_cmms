from rest_framework import routers, viewsets

from .models import AssetCategory, Asset, AssetAttachment, AssetSparePartLink
from .serializers import (
    AssetCategorySerializer,
    AssetSerializer,
    AssetAttachmentSerializer,
    AssetSparePartLinkSerializer,
)


class AssetCategoryViewSet(viewsets.ModelViewSet):
    queryset = AssetCategory.objects.all()
    serializer_class = AssetCategorySerializer


class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.select_related('plant', 'location').all()
    serializer_class = AssetSerializer


class AssetAttachmentViewSet(viewsets.ModelViewSet):
    queryset = AssetAttachment.objects.all()
    serializer_class = AssetAttachmentSerializer


class AssetSparePartLinkViewSet(viewsets.ModelViewSet):
    queryset = AssetSparePartLink.objects.all()
    serializer_class = AssetSparePartLinkSerializer


router = routers.DefaultRouter()
router.register(r'categories', AssetCategoryViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'attachments', AssetAttachmentViewSet)
router.register(r'spare-parts', AssetSparePartLinkViewSet)

urlpatterns = router.urls