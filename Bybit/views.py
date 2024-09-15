from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from .utlis import bybit_ref
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


@swagger_auto_schema(method='post',
                     request_body=VerifyUserSerializer,
                     responses={200: VerifyUserResponseSerializer})
@api_view(['POST'])
def verify_user(request):
    serializer = VerifyUserSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        print(1)
        telegram_id = serializer.validated_data['telegram_id']
        bybit_id = serializer.validated_data['bybit_id']
        referral_id = serializer.validated_data.get('referral_id')
        RegisteredWithReferral = bool(referral_id)
        registered, traded_volume = bybit_ref(bybit_id)
        print(registered, traded_volume)
        if registered:
            user, created = User.objects.update_or_create(
                TelegramId=telegram_id,
                defaults={'BybitId': bybit_id, 'Balance': traded_volume, 'RegisteredWithReferral': RegisteredWithReferral},
            )
            return JsonResponse({'success': True, 'message': 'User verified', 'traded_volume': traded_volume})
        else:
            return JsonResponse({'success': False, 'message': 'User not registered with referral'})

    return JsonResponse({'error': 'Invalid request method'})



@api_view(['GET'])
def list_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def get_user_by_telegram_id(request, telegram_id):
    try:
        user = User.objects.get(TelegramId=telegram_id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['DELETE'])
def delete_user_by_id(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)


@swagger_auto_schema(method='post',
                     request_body=FeesRequestSerializer,
                     responses={200: FeesResponseSerializer})
@api_view(['POST'])
def fee_amount(request):
    serializer = FeesRequestSerializer(data=request.data)
    if serializer.is_valid():
        bybit_id = serializer.validated_data['bybit_id']

        registered, traded_volume = bybit_ref(bybit_id)
        print(registered, traded_volume)
        if registered:
            fees = (float(traded_volume.get('result').get('takerVol365Day')) * 0.001
                    + float(traded_volume.get('result').get('makerVol365Day')) * 0.0003)
            tax = fees * 2
            return JsonResponse({'success': True, 'Fees': fees, 'Tax': tax}, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Failed to retrieve data from Bybit API'}, status=500)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid input'}, status=400)


@swagger_auto_schema(method='post',
                     request_body=InviteRequestSerializer,
                     responses={200: InviteResponseSerializer})
@api_view(['POST'])
def get_invitation_link(request):
    serializer = InviteRequestSerializer(data=request.data)
    if serializer.is_valid():
        return JsonResponse({'success': True,
                         'link': 'https://t.me/TaxCoinBot?start=referral_{}'.format(serializer.validated_data['telegram_id'])},
                            status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid input', 'details': serializer.errors}, status=400)