# Generated by Django 3.1.3 on 2020-11-27 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sent_messages', '0003_auto_20201109_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='alert',
            field=models.IntegerField(default=0),
        ),
    ]