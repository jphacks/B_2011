from django.contrib import admin

# Register your models here.
from examinees.models import Examinee

@admin.register(
    Examinee
)
class ContestAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Examinee._meta.fields]
