from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from api.models import User
from api.permissions import IsActiveUser, IsNonActiveUser
from utils import messages

from api.serializers import (
    UserRegisterSerializer,
    UserLoginSerializer,
    UserListSerializer,
    UserUpdateSerializer,
    UserUpdatePasswordSerializer,
)


class UserViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    def get_permissions(self):
        if self.action in ["login", "create"]:
            self.permission_classes = (AllowAny,)
        if self.action in [
            "list",
            "update_profile",
            "update_password",
        ]:
            self.permission_classes = (IsAuthenticated,)
        if self.action == "deactivate_profile":
            self.permission_classes = (IsAuthenticated, IsActiveUser)
        if self.action == "activate_profile":
            self.permission_classes = [IsAuthenticated, IsNonActiveUser]

        return super().get_permissions()

    def get_queryset(self):
        return User.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return UserRegisterSerializer
        elif self.action == "login":
            return UserLoginSerializer
        elif self.action == "update_profile":
            return UserUpdateSerializer
        elif self.action == "update_password":
            return UserUpdatePasswordSerializer
        return UserListSerializer

    @action(methods=["POST"], detail=False)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data)

    @action(methods=["PUT"], detail=False)
    def update_profile(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(methods=["GET"], detail=False)
    def deactivate_profile(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'message': messages.USER_DEACTIVATED})

    @action(methods=["GET"], detail=False)
    def activate_profile(self, request, *args, **kwargs):
        user = request.user
        user.is_active = True
        user.save()
        return Response({'message': messages.USER_ACTIVATED})

    @action(methods=["PUT"], detail=False)
    def update_password(self, request, *args, **kwargs):
        user = request.user
        serializer = self.get_serializer(user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': messages.PASSWORD_UPDATED})
