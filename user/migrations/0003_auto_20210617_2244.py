# Generated by Django 2.2 on 2021-06-18 05:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_message_created_for'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='created_for',
            field=models.IntegerField(),
        ),
    ]
