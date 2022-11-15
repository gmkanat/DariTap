from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.models import Wishlist
from api.serializers import WishlistSerializer


class WishlistViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.CreateModelMixin,
    viewsets.mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    search_fields = ["item__name", "item__description"]
    filter_fields = ["item__category__name"]
    order_fields = ["item__name", "item__price", "item__category__name"]

    def get_permissions(self):
        self.permission_classes = [
            IsAuthenticated,
        ]
        return super().get_permissions()

    def get_queryset(self):
        return Wishlist.objects.filter(is_active=True)

    def get_serializer_class(self):
        return WishlistSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user=request.user)
        instance = get_object_or_404(queryset, pk=kwargs['pk'])
        instance.is_active = False
        instance.save()
        return Response(status=204)

