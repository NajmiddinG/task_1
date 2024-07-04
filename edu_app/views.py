from rest_framework import viewsets, permissions
from .models import User, Branch, ClassSchedule, Request
from .serializers import UserSerializer, BranchSerializer, ClassScheduleSerializer, RequestSerializer

class IsSuperuserOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.role == 'superuser' or request.user.role == 'branch_admin')

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsSuperuserOrAdmin()]
        return super().get_permissions()

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [IsSuperuserOrAdmin]

class ClassScheduleViewSet(viewsets.ModelViewSet):
    queryset = ClassSchedule.objects.all()
    serializer_class = ClassScheduleSerializer
    permission_classes = [IsSuperuserOrAdmin]

class RequestViewSet(viewsets.ModelViewSet):
    queryset = Request.objects.all()
    serializer_class = RequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(student=self.request.user)

    def get_queryset(self):
        if self.request.user.role == 'student':
            return Request.objects.filter(student=self.request.user)
        return super().get_queryset()
