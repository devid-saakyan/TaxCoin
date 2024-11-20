import uuid

from django.db import models


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    TelegramId = models.BigIntegerField(unique=True)
    OKXId = models.CharField(unique=True, max_length=50)
    Balance = models.FloatField()
    RegistrationDate = models.DateTimeField(auto_now_add=True)
    RegisteredWithReferral = models.BooleanField(default=False)
    points = models.IntegerField(default=0)


class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals', to_field='TelegramId')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referred_by', to_field='TelegramId')
    date_referred = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.referrer.TelegramId} referred {self.referred_user.TelegramId}"


class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    reward_points = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    icon = models.ImageField(upload_to='icons/', blank=True, null=True)

    def __str__(self):
        return self.title


class UserTask(models.Model):
    telegram_user_id = models.CharField(max_length=50)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.telegram_user_id} - {self.task.title}"