# Generated by Django 5.1.1 on 2025-02-12 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_profile_contact_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_profile',
            name='country',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
