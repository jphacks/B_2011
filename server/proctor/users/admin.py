from django.contrib import admin

# Register your models here.
from users.models import User


@admin.register(
    User
)
class ContestAdmin(admin.ModelAdmin):
    list_display = [f.name for f in User._meta.fields]