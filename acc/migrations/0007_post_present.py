# Generated by Django 3.1.7 on 2021-03-08 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acc', '0006_auto_20210308_1400'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='present',
            field=models.BooleanField(default=False),
        ),
    ]
