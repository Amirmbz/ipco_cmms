from rest_framework import routers, viewsets

from .models import Plant
from .serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer


router = routers.DefaultRouter()
router.register(r'plants', PlantViewSet)

urlpatterns = router.urls