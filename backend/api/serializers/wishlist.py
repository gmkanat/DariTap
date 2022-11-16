from rest_framework import serializers

from api.models import Wishlist
from api.serializers import ItemListSerializer
from utils import messages


class WishlistSerializer(serializers.ModelSerializer):
    item = ItemListSerializer(read_only=True)
    item_id = serializers.IntegerField(source='item', write_only=True)

    class Meta:
        model = Wishlist
        fields = (
            'id',
            'item',
            'item_id',
        )

    def validate(self, attrs):
        if Wishlist.objects.filter(
                user=self.context['request'].user,
                item=attrs['item'],
        ).exists():
            raise serializers.ValidationError(
                messages.ITEM_ALREADY_IN_WISHLIST
            )
        return attrs

    def create(self, validated_data):
        wishlist = Wishlist.objects.create(
            item_id=validated_data['item'],
            user=self.context['request'].user,
        )
        return wishlist
