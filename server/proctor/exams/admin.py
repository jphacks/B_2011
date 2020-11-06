from django.contrib import admin

# Register your models here.
from exams.models import Exam

@admin.register(
    Exam
)
class ContestAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Exam._meta.fields]
