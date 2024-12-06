from django.contrib import admin
from .models import UserState

@admin.register(UserState)
class UserStateAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'state', 'bybit_status', 'okx_status', 'updated_at', )
