# Bybit.serializers.py

from rest_framework import serializers
from Bybit.models import User
from .models import Task, UserTask, UserWallet

class VerifyUserSerializer(serializers.Serializer):
    telegram_id = serializers.IntegerField()
    bybit_id = serializers.CharField(max_length=255)
    referral_id = serializers.CharField(max_length=100, required=False, allow_blank=True, allow_null=True)
    nickname = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    firstname = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    lastname = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    photo_url = serializers.URLField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        ref_name = "BybitVerifyUser"

class VerifyUserResponseSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    message = serializers.CharField(max_length=255)
    traded_volume = serializers.FloatField(required=False)
    registered_with_referral = serializers.BooleanField(required=False)

    class Meta:
        ref_name = "BybitVerifyUserResponse"

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        ref_name = "BybitUser"

class FeesRequestSerializer(serializers.Serializer):
    bybit_id = serializers.CharField(max_length=100, required=True)

    class Meta:
        ref_name = "BybitFeesRequest"

class FeesResponseSerializer(serializers.Serializer):
    Fees = serializers.FloatField()
    Tax = serializers.FloatField()

    class Meta:
        ref_name = "BybitFeesResponse"

class InviteRequestSerializer(serializers.Serializer):
    telegram_id = serializers.CharField(max_length=100, required=True)

    class Meta:
        ref_name = "BybitInviteRequest"

class InviteResponseSerializer(serializers.Serializer):
    link = serializers.CharField(max_length=100)

    class Meta:
        ref_name = "BybitInviteResponse"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'reward_points', 'is_active', 'icon']
        ref_name = "BybitTask"

class UserTaskSerializer(serializers.ModelSerializer):
    task = TaskSerializer()

    class Meta:
        model = UserTask
        fields = ['task', 'is_completed', 'completed_at']
        ref_name = "BybitUserTask"

class BybitKeyCheckSerializer(serializers.Serializer):
    api_key = serializers.CharField(max_length=100)
    api_secret = serializers.CharField(max_length=100)

    class Meta:
        ref_name = "BybitKeyCheck"


class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWallet
        fields = ['telegram_id', 'wallet_address']