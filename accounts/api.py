from rest_framework import routers, viewsets
from django.contrib.auth.models import User

from .models import Department, Role, UserProfile
from .serializers import DepartmentSerializer, RoleSerializer, UserProfileSerializer


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.select_related('user').all()
    serializer_class = UserProfileSerializer


router = routers.DefaultRouter()
router.register(r'departments', DepartmentViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'user-profiles', UserProfileViewSet)

urlpatterns = router.urls