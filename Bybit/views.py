from django.shortcuts import render
from django.http import JsonResponse
from .models import User
from .utlis import bybit_ref
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
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
        registered, traded_volume = bybit_ref(bybit_id)
        print(registered, traded_volume)
        if registered:
            user, created = User.objects.update_or_create(
                TelegramId=telegram_id,
                defaults={'BybitId': bybit_id, 'Balance': traded_volume, 'RegisteredWithReferral': True}
            )
            return JsonResponse({'success': True, 'message': 'User verified', 'traded_volume': traded_volume})
        else:
            return JsonResponse({'success': False, 'message': 'User not registered with referral'})

    return JsonResponse({'error': 'Invalid request method'})