from django.db import models
from django.utils.timezone import now


class UserState(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    state = models.IntegerField(
        choices=[
            (1, "State 1"),
            (2, "State 2"),
        ],
        default=1,
    )
    bybit_status = models.BooleanField(default=False)
    okx_status = models.BooleanField(default=False)
    updated_at = models.DateTimeField(default=now)

    def __str__(self):
        return f"Telegram ID: {self.telegram_id}, State: {self.state}, Bybit: {self.bybit_status}, OKX: {self.okx_status}"


class ExchangeAPIKey(models.Model):
    EXCHANGE_CHOICES = [
        ('bybit', 'Bybit'),
        ('okx', 'OKX'),
    ]

    telegram_id = models.BigIntegerField()
    exchange = models.CharField(max_length=10, choices=EXCHANGE_CHOICES)
    api_key = models.CharField(max_length=255)
    api_secret = models.CharField(max_length=255)
    passphrase = models.CharField(max_length=255, null=True, blank=True)
    expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('telegram_id', 'exchange')

    def __str__(self):
        return f"{self.telegram_id} - {self.exchange}"