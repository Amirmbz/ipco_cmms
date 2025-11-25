from rest_framework import routers, viewsets

from .models import Notification
from .serializers import NotificationSerializer


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


router = routers.DefaultRouter()
router.register(r'notifications', NotificationViewSet)

urlpatterns = router.urls