# Generated by Django 5.1.1 on 2024-10-21 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0011_notification_another_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Online',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('is_online', models.BooleanField(default=False)),
                ('last_active', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]