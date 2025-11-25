from rest_framework import routers, viewsets

from .models import Warehouse, PartCategory, Part, PartStock, PartTransaction
from .serializers import (
    WarehouseSerializer,
    PartCategorySerializer,
    PartSerializer,
    PartStockSerializer,
    PartTransactionSerializer,
)


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.select_related('plant', 'location').all()
    serializer_class = WarehouseSerializer


class PartCategoryViewSet(viewsets.ModelViewSet):
    queryset = PartCategory.objects.all()
    serializer_class = PartCategorySerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class PartStockViewSet(viewsets.ModelViewSet):
    queryset = PartStock.objects.select_related('part', 'warehouse').all()
    serializer_class = PartStockSerializer


class PartTransactionViewSet(viewsets.ModelViewSet):
    queryset = PartTransaction.objects.select_related('part').all()
    serializer_class = PartTransactionSerializer


router = routers.DefaultRouter()
router.register(r'warehouses', WarehouseViewSet)
router.register(r'part-categories', PartCategoryViewSet)
router.register(r'parts', PartViewSet)
router.register(r'stock', PartStockViewSet)
router.register(r'transactions', PartTransactionViewSet)

urlpatterns = router.urls