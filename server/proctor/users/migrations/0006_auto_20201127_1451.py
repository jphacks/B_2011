# Generated by Django 3.1.3 on 2020-11-27 05:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20201127_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_id',
            field=models.UUIDField(default=uuid.UUID('2c1c0062-ef06-48a8-8571-9d93b895a64e'), editable=False, primary_key=True, serialize=False),
        ),
    ]
