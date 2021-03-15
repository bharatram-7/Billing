# Generated by Django 3.1.7 on 2021-03-15 16:42

import datetime
from django.db import migrations, models
from django.utils.timezone import utc
import rolestest.validators


class Migration(migrations.Migration):

    dependencies = [
        ('rolestest', '0007_auto_20210312_2108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d', validators=[rolestest.validators.image_restriction]),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 15, 16, 42, 1, 857665, tzinfo=utc)),
        ),
    ]
