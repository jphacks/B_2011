# Generated by Django 3.1.3 on 2020-11-27 05:31

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20201109_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('2eba23a2-1e9c-4559-8630-3e1076b96d79'), editable=False, primary_key=True, serialize=False),
        ),
    ]
