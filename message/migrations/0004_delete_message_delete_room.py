# Generated by Django 5.1.1 on 2024-10-03 16:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0003_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
        migrations.DeleteModel(
            name='Room',
        ),
    ]
