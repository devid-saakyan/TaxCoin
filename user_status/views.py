from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.timezone import now
from .models import UserState, ExchangeAPIKey
from .serializers import UserStateSerializer, ExchangeAPIKeySerializer
from okx.models import User as OKXUser
from Bybit.models import User as BybitUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class GetUserStateController(APIView):

    @swagger_auto_schema(
        operation_summary="Получить состояние пользователя",
        manual_parameters=[
            openapi.Parameter(
                'telegram_id', openapi.IN_PATH,
                description="Telegram ID пользователя",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'telegram_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Telegram ID"),
                    'state': openapi.Schema(type=openapi.TYPE_INTEGER, description="Состояние пользователя"),
                    'updated_at': openapi.Schema(type=openapi.FORMAT_DATETIME, description="Дата последнего обновления"),
                    'BybitStatus': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Зарегистрирован ли пользователь в Bybit"),
                    'OKXStatus': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Зарегистрирован ли пользователь в OKX"),
                }
            ),
            404: "User state not found",
            400: "Bad request"
        }
    )
    def get(self, request, telegram_id=None):
        if not telegram_id:
            return Response({'error': 'TelegramId is required'}, status=status.HTTP_400_BAD_REQUEST)

        okx_status = OKXUser.objects.filter(TelegramId=telegram_id).exists()
        bybit_status = BybitUser.objects.filter(TelegramId=telegram_id).exists()

        try:
            user_state = UserState.objects.get(telegram_id=telegram_id)
            serializer = UserStateSerializer(user_state)
            state_data = serializer.data
        except UserState.DoesNotExist:
            state_data = None

        response_data = {
            'telegram_id': telegram_id,
            'state': state_data.get('state') if state_data else None,
            'updated_at': state_data.get('updated_at') if state_data else None,
            'BybitStatus': bybit_status,
            'OKXStatus': okx_status,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class PostUserStateController(APIView):
    @swagger_auto_schema(
        operation_summary="Обновить состояние пользователя",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'telegram_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Telegram ID пользователя"),
                'state': openapi.Schema(type=openapi.TYPE_INTEGER, description="Новое состояние пользователя"),
            },
            required=['telegram_id', 'state']
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description="Результат операции"),
                    'telegram_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="Telegram ID"),
                    'state': openapi.Schema(type=openapi.TYPE_INTEGER, description="Обновленное состояние"),
                    'updated_at': openapi.Schema(type=openapi.FORMAT_DATETIME,
                                                 description="Дата последнего обновления"),
                }
            ),
            400: "Bad request"
        }
    )
    def post(self, request):
        telegram_id = request.data.get('telegram_id')
        state = request.data.get('state')

        if not telegram_id or state is None:
            return Response({'error': 'telegram_id and state are required'}, status=status.HTTP_400_BAD_REQUEST)

        user_state, created = UserState.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={'state': state}
        )

        serializer = UserStateSerializer(user_state)
        response_data = {
            'message': "State created successfully" if created else "State updated successfully",
            'telegram_id': telegram_id,
            'state': serializer.data.get('state'),
            'updated_at': serializer.data.get('updated_at'),
        }

        return Response(response_data, status=status.HTTP_200_OK)


class AddOrUpdateAPIKeyView(APIView):

    @swagger_auto_schema(request_body=ExchangeAPIKeySerializer)
    def post(self, request):
        serializer = ExchangeAPIKeySerializer(data=request.data)
        if serializer.is_valid():
            obj, created = ExchangeAPIKey.objects.update_or_create(
                telegram_id=serializer.validated_data['telegram_id'],
                exchange=serializer.validated_data['exchange'],
                defaults={
                    'api_key': serializer.validated_data['api_key'],
                    'api_secret': serializer.validated_data['api_secret'],
                    'passphrase': serializer.validated_data['passphrase'],
                    'expired': serializer.validated_data.get('expired', False),
                }
            )
            return Response({
                'success': True,
                'created': created,
                'data': ExchangeAPIKeySerializer(obj).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckAPIKeyView(APIView):

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('telegram_id', openapi.IN_QUERY, type=openapi.TYPE_INTEGER, required=True),
            openapi.Parameter('exchange', openapi.IN_QUERY, type=openapi.TYPE_STRING, enum=['bybit', 'okx'], required=True),
        ]
    )
    def get(self, request):
        telegram_id = request.GET.get('telegram_id')
        exchange = request.GET.get('exchange')

        if not telegram_id or not exchange:
            return Response({'error': 'telegram_id and exchange are required'}, status=status.HTTP_400_BAD_REQUEST)

        exists = ExchangeAPIKey.objects.filter(telegram_id=telegram_id, exchange=exchange).exists()
        return Response({
            'telegram_id': telegram_id,
            'exchange': exchange,
            'has_keys': exists
        }, status=status.HTTP_200_OK)