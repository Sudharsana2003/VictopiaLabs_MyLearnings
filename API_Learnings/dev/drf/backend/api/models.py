# models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from rest_framework.authtoken.models import Token

class TokenWithExpiry(Token):
    expires_at = models.DateTimeField(
        default=timezone.now() + timedelta(days=7)
    )  # default: token valid for 7 days

    class Meta:
        verbose_name = "Token with Expiry"
        verbose_name_plural = "Tokens with Expiry"
