from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import User
from api.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserListSerializer,
)


class UserViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet
):

    def get_permissions(self):
        if self.action in ['login', 'create']:
            self.permission_classes = (AllowAny, )
        if self.action == 'list':
            self.permission_classes = (IsAuthenticated, )
        return super().get_permissions()

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegisterSerializer
        elif self.action == 'login':
            return UserLoginSerializer
        return UserListSerializer

    @action(methods=['POST'], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)


