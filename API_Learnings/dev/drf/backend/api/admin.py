# admin.py
from django.contrib import admin
from .models import TokenWithExpiry

@admin.register(TokenWithExpiry)
class TokenWithExpiryAdmin(admin.ModelAdmin):
    list_display = ("user", "key", "created", "expires_at")
    readonly_fields = ("key", "created")
