# Generated by Django 3.1.7 on 2021-03-19 09:33

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('rolestest', '0008_auto_20210315_2212'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='user_activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='order',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 19, 9, 33, 12, 837031, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='purchaseditem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='purchased_items', to='rolestest.order'),
        ),
    ]
