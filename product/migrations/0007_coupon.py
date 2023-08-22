# Generated by Django 4.2.3 on 2023-07-27 11:18

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0006_rename_storeage_productvariant_storage"),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
            fields=[
                (
                    "uid",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("coupen_code", models.CharField(max_length=10)),
                ("is_expired", models.BooleanField(default=False)),
                ("discount_price", models.IntegerField(default=100)),
                ("minimum_amount", models.IntegerField(default=500)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
