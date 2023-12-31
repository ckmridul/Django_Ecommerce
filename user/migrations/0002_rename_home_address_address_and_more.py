# Generated by Django 4.2.3 on 2023-08-03 07:03

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="address",
            old_name="home",
            new_name="address",
        ),
        migrations.RenameField(
            model_name="address",
            old_name="alternative_number",
            new_name="alternate_number",
        ),
        migrations.AlterField(
            model_name="address",
            name="landmark",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
