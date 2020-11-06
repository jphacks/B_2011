from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Examinee(models.Model):
    class Meta:
        db_table = 'examinee'

    examinee_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    exam_id = models.UUIDField()
    created_at = models.DateTimeField(default=timezone.now)