from rest_framework import serializers


class VerifyUserSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    bybit_id = serializers.CharField(max_length=255)


class VerifyUserResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=255)
    traded_volume = serializers.FloatField(required=False)
    registered_with_referral = serializers.BooleanField(required=False)