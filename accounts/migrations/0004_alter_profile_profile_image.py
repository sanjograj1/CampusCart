# Generated by Django 5.0.1 on 2024-02-18 05:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_alter_profile_profile_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(
                default="profile_images/default.png", upload_to="profile_images/"
            ),
        ),
    ]