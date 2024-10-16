from django.contrib import admin
from .models import Task, UserTask, User


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