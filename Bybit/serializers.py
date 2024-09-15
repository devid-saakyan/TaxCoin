from rest_framework import serializers

from Bybit.models import User


class VerifyUserSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    bybit_id = serializers.CharField(max_length=255)
    referral_id = serializers.CharField(max_length=100, required=False, allow_blank=True)


class VerifyUserResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=255)
    traded_volume = serializers.FloatField(required=False)
    registered_with_referral = serializers.BooleanField(required=False)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FeesRequestSerializer(serializers.Serializer):
    bybit_id = serializers.CharField(max_length=100, required=True)


class FeesResponseSerializer(serializers.Serializer):
    Fees = serializers.FloatField()
    Tax = serializers.FloatField()


class InviteRequestSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(max_length=100, required=True)


class InviteResponseSerializer(serializers.Serializer):
    link = serializers.CharField(max_length=100)