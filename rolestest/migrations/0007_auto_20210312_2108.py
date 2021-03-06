# Generated by Django 3.1.7 on 2021-03-12 15:38

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rolestest', '0006_auto_20210312_1621'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={'permissions': [('can_manage_carts', 'Can view, create, edit, or delete cart items')]},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'permissions': [('can_view_items', 'Can view all items'), ('can_manage_items', 'Can create, edit, or delete items')], 'verbose_name': 'item', 'verbose_name_plural': 'items'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'permissions': [('can_view_menus', 'Can view all menus'), ('can_manage_menus', 'Can create, edit, or delete menus')], 'verbose_name': 'menu', 'verbose_name_plural': 'menus'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('can_view_orders', 'Can view his/her orders'), ('can_view_all_orders', 'Can view all orders')]},
        ),
        migrations.AlterModelOptions(
            name='purchaseditem',
            options={'permissions': [('can_view_purchased_items', 'Can view his/her purchased items'), ('can_view_all_purchased_items', 'Can view all purchased items')]},
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 12, 15, 38, 37, 549106, tzinfo=utc)),
        ),
    ]
