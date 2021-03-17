from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


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


class OrderListSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Order
        fields = '__all__'
