# Generated by Django 4.2.3 on 2023-08-04 11:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0008_rename_coupen_code_coupon_coupon_code"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("user", "0003_address_name"),
        ("order", "0002_remove_orderproduct_order_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
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
                ("order_number", models.CharField(max_length=20)),
                (
                    "order_total",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("order placed", "order placed"),
                            ("shipped", "shipped"),
                            ("Deliverd", "Deliverd"),
                            ("Cancel", "Cancel"),
                        ],
                        default="order placed",
                        max_length=15,
                    ),
                ),
                ("is_orderd", models.BooleanField(default=False)),
                (
                    "address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="user.address"
                    ),
                ),
                (
                    "payment",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="order.payment",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="OrderProduct",
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
                ("quantity", models.IntegerField()),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orderproduct",
                        to="order.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.product",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "variation",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="product.productvariant",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
