# Generated by Django 3.1.3 on 2020-11-27 05:52

from django.db import migrations, models
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('exam_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('user_id', models.UUIDField()),
                ('exam_name', models.CharField(default=None, max_length=200, null=True)),
                ('description', models.CharField(default=None, max_length=200, null=True)),
                ('exam_url', models.URLField()),
                ('exam_date', models.DateField()),
                ('start_at', models.DateTimeField()),
                ('end_at', models.DateTimeField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
            ],
            options={
                'db_table': 'exam',
            },
        ),
    ]
