# Generated by Django 4.2.3 on 2023-08-07 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0003_address_name"),
        ("order", "0003_order_orderproduct"),
    ]

    operations = [
        migrations.RenameField(
            model_name="payment",
            old_name="ammount_paind",
            new_name="amount_paid",
        ),
        migrations.AlterField(
            model_name="order",
            name="address",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="user.address"
            ),
        ),
    ]
