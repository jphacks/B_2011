from django.db import models
from django.utils import timezone
import uuid


# Create your models here.
class Message(models.Model):
    class Meta:
        db_table = 'message'

    message_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    examinee_id = models.UUIDField()
    exam_id = models.UUIDField()
    module_name = models.CharField(max_length=100, blank=True, null=True)
    alert = models.BooleanField(default=False)
    description = models.CharField(max_length=200, default=None, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
