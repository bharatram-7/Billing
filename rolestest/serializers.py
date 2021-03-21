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


class MenuWithItemsSerializer(serializers.ModelSerializer):
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = Menu
        fields = '__all__'
        read_only_fields = ['items']

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name')
        instance.active = validated_data.get('active')
        instance.save()
        try:
            if not instance.active:
                items = Item.objects.filter(menu__id=instance.id)
                for item in items:
                    print(item.name)
                    cart_items = CartItem.objects.filter(item=item)
                    if cart_items:
                        for cart_item in cart_items:
                            cart_item.delete()
            return instance
        except:
            return instance


class MenuSerializer(serializers.ModelSerializer):

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
    quantity = serializers.IntegerField(min_value=0, max_value=100)

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
        # items = []
        # for item in Item.objects.only('name'):
        #     items.append(item.name)
        # try:
        #     for item in purchased_items:
        #         if item["item"] in items:
        #             item["order"] = order
        #             PurchasedItem.objects.create(**item)
        #     return order
        # except Exception as e:
        #     order.delete()
        #     return

        items = {}
        active_menus = Menu.objects.filter(active=True)
        for menu in active_menus:
            active_items = Item.objects.filter(menu__id=menu.id)
            for item in active_items:
                items[item.name] = item.price
        print(items)
        try:
            for item in purchased_items:
                if items[item["item"]] == item["price"]:
                    item["order"] = order
                    PurchasedItem.objects.create(**item)
            return order
        except:
            raise serializers.ValidationError("Invalid items")

    def validate(self, data):
        """
        Check that purchased items exist
        """
        if not data['purchased_items']:
            raise serializers.ValidationError("There needs to be at least one item to create an order")
        return data


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['date', 'total', 'rating', 'user']


class OrderRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    rating = serializers.IntegerField()
    status = serializers.CharField(read_only=True)

    def validate_rating(self, value):

        if self.instance.status == "P":
            raise serializers.ValidationError('You can only rate a Delivered order')

        if value is None:
            raise serializers.ValidationError('This field is required')

        if value > 5 or value < 1:
            raise serializers.ValidationError('Please select a value between 1 and 5 inclusive')

        return value

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['date', 'total', 'status']