import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TelegramId = models.BigIntegerField(unique=True)
    BybitId = models.CharField(unique=True, max_length=50)
    Balance = models.FloatField()
    RegistrationDate = models.DateTimeField(auto_now_add=True)
    RegisteredWithReferral = models.BooleanField(default=False)
