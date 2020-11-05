from django.contrib import admin

# Register your models here.
from sent_messages.models import Message


@admin.register(
    Message
)
class ContestAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Message._meta.fields]