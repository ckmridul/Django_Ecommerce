# Generated by Django 4.2.3 on 2023-07-27 13:34

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("product", "0007_coupon"),
    ]

    operations = [
        migrations.RenameField(
            model_name="coupon",
            old_name="coupen_code",
            new_name="coupon_code",
        ),
    ]
