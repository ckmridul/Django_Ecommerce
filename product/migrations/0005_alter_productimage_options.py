# Generated by Django 4.2.3 on 2023-07-24 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_productimage_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['-image']},
        ),
    ]
