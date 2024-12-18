# Generated by Django 5.1.1 on 2024-11-04 06:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0014_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MesssageView',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.IntegerField()),
                ('view', models.BooleanField(default=False)),
                ('chat_room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='message.chatroom')),
            ],
        ),
    ]
