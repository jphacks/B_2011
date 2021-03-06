# Generated by Django 3.1.3 on 2020-11-09 07:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('examinees', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examinee',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='examinee',
            name='exam_id',
            field=models.UUIDField(editable=False),
        ),
    ]
