# Generated by Django 2.2 on 2021-06-18 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='created_for',
            field=models.CharField(default='none', max_length=255),
            preserve_default=False,
        ),
    ]
