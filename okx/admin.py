from django.contrib import admin
from .models import Task, UserTask, User, Referral, UserState

admin.site.site_header = ("TAXCOIN admin")       # Заголовок на главной странице админки
admin.site.site_title = ("Your Custom Title")         # Заголовок на вкладке браузера


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'reward_points', 'is_active', 'created_at')


@admin.register(UserTask)
class UserTaskAdmin(admin.ModelAdmin):
    list_display = ('telegram_user_id', 'task', 'is_completed', 'completed_at')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('TelegramId', 'RegisteredWithReferral')


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('referrer_telegram_id', 'referred_user_telegram_id', 'date_referred')

    def referrer_telegram_id(self, obj):
        return obj.referrer.TelegramId

    def referred_user_telegram_id(self, obj):
        return obj.referred_user.TelegramId


@admin.register(UserState)
class UserStateAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'state', )