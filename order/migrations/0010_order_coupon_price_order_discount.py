# Generated by Django 4.2.3 on 2023-08-14 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0009_alter_order_options"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="coupon_price",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="order",
            name="discount",
            field=models.IntegerField(default=0),
        ),
    ]
