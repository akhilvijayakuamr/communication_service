# Generated by Django 5.1.1 on 2024-10-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0010_remove_notification_another_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='another_user',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
