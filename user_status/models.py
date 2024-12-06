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
