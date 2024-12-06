from rest_framework import serializers
from .models import UserState


class UserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserState
        fields = ['telegram_id', 'state', 'bybit_status', 'okx_status', 'updated_at']
