from rest_framework import serializers

from api.models import Item, Image, Category


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='image.url')

    class Meta:
        model = Image
        fields = (
            'id',
            'image',
        )


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            'id',
            'name',
        )


class ItemListSerializer(serializers.ModelSerializer):
    image = serializers.CharField(source='images.first.image.url')
    category = CategorySerializer(
        read_only=True,
    )
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'description',
            'price',
            'image',
            'category',
            'is_favorite',
        )

    def get_is_favorite(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.wishlists.filter(user=self.context['request'].user).exists()
        return False


class ItemDetailSerializer(serializers.ModelSerializer):
    images = ImageSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    is_favorite = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'description',
            'price',
            'images',
            'category',
            'is_favorite',
        )

    def get_is_favorite(self, obj):
        if self.context['request'].user.is_authenticated:
            return obj.wishlists.filter(user=self.context['request'].user).exists()
        return False
