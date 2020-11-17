from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Exam(models.Model):
    class Meta:
        db_table = 'exam'

    exam_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user_id = models.UUIDField()
    exam_name = models.CharField(max_length=200, default=None, null=True)
    description = models.CharField(max_length=200, default=None, null=True)
    exam_date = models.DateField()
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)
