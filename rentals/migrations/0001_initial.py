# Generated by Django 5.0.1 on 2024-03-15 03:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rental',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('property_name', models.CharField(max_length=50)),
                ('property_image', models.ImageField(default='upload_property/property_sample.jpg', upload_to='upload_property/')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('seller', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]