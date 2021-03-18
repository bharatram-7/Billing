from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email']


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'


class ViewCartSerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity']


class CreateCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity', 'user']
        validators = [
            UniqueTogetherValidator(
                queryset=CartItem.objects.all(),
                fields=['item', 'user'],
                message="This item is already present in the user's cart"
            )
        ]


class UpdateDeleteCartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = CartItem
        fields = ['id', 'item', 'quantity', 'user']


class PurchasedItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchasedItem
        fields = '__all__'
        extra_kwargs = {
            'order': {'required': False}
        }


class OrderWithItemsSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    purchased_items = PurchasedItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['date']

    def create(self, validated_data):
        purchased_items = validated_data.pop('purchased_items')
        order = Order.objects.create(**validated_data)
        items = []
        for item in Item.objects.only('name'):
            items.append(item.name)
        try:
            for item in purchased_items:
                if item["item"] in items:
                    item["order"] = order
                    PurchasedItem.objects.create(**item)
            return order
        except Exception as e:
            order.delete()
            return

    def validate(self, data):
        """
        Check that purchased items exist
        """
        if not data['purchased_items']:
            raise serializers.ValidationError("There needs to be at least one item to create an order")
        return data


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['date', 'total']

