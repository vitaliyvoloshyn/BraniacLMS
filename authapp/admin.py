from django.contrib import admin
from .models import *


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ["id", "username", "email", "is_active", "date_joined"]
    ordering = ["-date_joined"]
