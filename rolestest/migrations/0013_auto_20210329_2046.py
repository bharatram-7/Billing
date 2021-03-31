# Generated by Django 3.1.7 on 2021-03-29 15:16

from django.db import migrations, models
import django.utils.timezone
import rolestest.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rolestest', '0012_auto_20210328_2236'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cartitem',
            options={},
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'item', 'verbose_name_plural': 'items'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name': 'menu', 'verbose_name_plural': 'menus'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={},
        ),
        migrations.AlterModelOptions(
            name='purchaseditem',
            options={},
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[rolestest.validators.price_restriction]),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='purchaseditem',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[rolestest.validators.price_restriction]),
        ),
    ]
