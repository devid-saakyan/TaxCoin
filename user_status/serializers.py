from rest_framework import serializers
from .models import UserState, ExchangeAPIKey


class UserStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserState
        fields = ['telegram_id', 'state', 'bybit_status', 'okx_status', 'updated_at']


class ExchangeAPIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeAPIKey
        fields = '__all__'