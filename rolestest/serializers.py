from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from .models import *
from django.contrib.auth.models import Group
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(queryset=Group.objects.all().exclude(name='Customers'),
                                          many=True, slug_field="name", required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'groups']

    def create(self, validated_data):
        groups = validated_data.pop("groups")
        if len(groups) > 1:
            raise serializers.ValidationError("User can't have more than one group")
        email = validated_data['email']
        name = validated_data['name']
        user = CustomUser(email=email, name=name)
        user.save()
        user.groups.set(groups)
        print(self.context)
        current_site = get_current_site(self.context['request'])
        subject = 'Activate your account'
        message = render_to_string('authentication/staff_activation_template.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return user

    def update(self, instance, validated_data):
        groups = ''
        user = CustomUser.objects.get(id=instance.id)
        current_group = instance.groups.all()[0].name
        # Since groups are optional
        if 'groups' in validated_data:
            groups = validated_data.pop('groups')
        if len(groups) > 1:
            raise serializers.ValidationError("User can't have more than one group")
        # Customer's group can't be edited
        if current_group == "Customers" and groups:
            raise serializers.ValidationError("Cannot change customer's roles")
        # Update group only if it's not the same as current group & can't edit another admin
        if groups and instance.groups.all()[0] != groups[0]:
            if current_group == "Admin":
                raise serializers.ValidationError("Cannot edit self/another admin's role")
            if instance.id != self.context['request'].user.id:
                user.groups.set(groups)

        instance.name = validated_data['name']
        if instance.email != validated_data['email']:
            instance.email = validated_data['email']
            user = instance.save()
            password = CustomUser.objects.make_random_password()
            user.set_password(password)
            user.save()
        else:
            instance.save()

        return CustomUser.objects.get(id=instance.id)
    

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
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
        read_only_fields = ['id', 'item', 'user']


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
    date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', required=False, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ['date', 'rating']

    def create(self, validated_data):
        purchased_items = validated_data.pop('purchased_items')
        order = Order.objects.create(**validated_data)
        items = {}
        no_item = True
        active_menus = Menu.objects.filter(active=True)
        for menu in active_menus:
            active_items = Item.objects.filter(menu__id=menu.id)
            for item in active_items:
                items[item.name] = item.price
        try:
            for item in purchased_items:
                if items[item["item"]] == item["price"]:
                    item["order"] = order
                    PurchasedItem.objects.create(**item)
                else:
                    order.delete()
                    raise serializers.ValidationError("Invalid items are found in the cart.")
            return order
        except Exception as e:
            order.delete()
            raise serializers.ValidationError("Invalid items are found in the cart.")

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