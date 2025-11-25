from rest_framework import routers, viewsets

from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.select_related('plant', 'parent').all()
    serializer_class = LocationSerializer


router = routers.DefaultRouter()
router.register(r'locations', LocationViewSet)

urlpatterns = router.urls