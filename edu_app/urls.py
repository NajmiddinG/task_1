from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, BranchViewSet, ClassScheduleViewSet, RequestViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'class-schedules', ClassScheduleViewSet)
router.register(r'requests', RequestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
