from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from api.models import Item, Category
from api.serializers import (
    ItemListSerializer,
    ItemDetailSerializer,
    CategorySerializer

)


class ItemViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    filter_backends = [
        filters.SearchFilter,
        DjangoFilterBackend,
        filters.OrderingFilter,
    ]
    filter_fields = ["category_id"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "price", "category__name"]

    def get_permissions(self):
        self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def get_queryset(self):
        return Item.objects.filter(is_active=True)

    def get_serializer_class(self):
        if self.action == 'list':
            return ItemListSerializer
        if self.action == 'retrieve':
            return ItemDetailSerializer


class CategoryViewSet(
    viewsets.mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    def get_permissions(self):
        self.permission_classes = [AllowAny, ]
        return super().get_permissions()

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def get_serializer_class(self):
        return CategorySerializer
