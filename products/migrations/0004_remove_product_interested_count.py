# Generated by Django 4.2.10 on 2024-02-18 12:23

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0003_product_interested_count"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="product",
            name="interested_count",
        ),
    ]
