# Generated by Django 5.0.1 on 2024-03-22 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_contact_message_alter_contact_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='course',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_class',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Class'),
        ),
    ]
