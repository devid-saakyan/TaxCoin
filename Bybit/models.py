import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TelegramId = models.BigIntegerField(unique=True)
    BybitId = models.CharField(unique=True, max_length=50)
    Balance = models.FloatField()
    RegistrationDate = models.DateTimeField(auto_now_add=True)
    RegisteredWithReferral = models.BooleanField(default=False)
    points = models.IntegerField(default=0)


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by')
    date_referred = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.TelegramId} referred {self.referred_user.TelegramId}"