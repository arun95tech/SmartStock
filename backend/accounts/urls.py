from rest_framework.routers import DefaultRouter
from .views import RoleViewSet, UserViewSet, PermissionViewSet, RolePermissionViewSet

router = DefaultRouter()
router.register('roles', RoleViewSet)
router.register('users', UserViewSet)
router.register('permissions', PermissionViewSet)
router.register('role-permissions', RolePermissionViewSet)

urlpatterns = router.urls