from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Referral
from .utlis import bybit_ref, check_bybit_keys, CheckKYC
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from rest_framework import viewsets, permissions
from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg import openapi
from django.db import IntegrityError



@swagger_auto_schema(method='post',
                     request_body=VerifyUserSerializer,
                     responses={200: VerifyUserResponseSerializer})
@api_view(['POST'])
def verify_user(request):
    serializer = VerifyUserSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        telegram_id = serializer.validated_data['telegram_id']
        bybit_id = serializer.validated_data['bybit_id']
        referral_id = serializer.validated_data.get('referral_id')
        RegisteredWithReferral = bool(referral_id)

        if referral_id:
            try:
                referral_id = int(referral_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid referral ID'}, status=400)

            referrer = User.objects.filter(TelegramId=referral_id).first()
            if referrer and referrer.referrals.filter(referred_user__TelegramId=telegram_id).exists():
                return JsonResponse({'error': 'Mutual referrals are not allowed'}, status=400)

        registered, traded_volume = bybit_ref(bybit_id)
        if registered:
            try:
                user, created = User.objects.update_or_create(
                    TelegramId=telegram_id,
                    defaults={
                        'BybitId': bybit_id,
                        'Balance': traded_volume,
                        'RegisteredWithReferral': RegisteredWithReferral
                    },
                )
                print(created)
                referrer = User.objects.filter(TelegramId=referral_id).first()
                print(referrer)
                if referral_id and created:
                    Referral.objects.create(referrer_id=referral_id, referred_user=user)

                return JsonResponse({'success': True, 'message': 'User verified', 'traded_volume': traded_volume})

            except IntegrityError as e:
                print(str(e))
                if 'BybitId' in str(e):
                    error_message = 'Bybit ID already exists.'
                elif 'TelegramId' in str(e):
                    error_message = 'Telegram ID already exists.'
                else:
                    error_message = 'A unique constraint failed.'

                return JsonResponse({'error': error_message}, status=400)

        else:
            return JsonResponse({'success': False, 'message': 'User not registered with referral'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@swagger_auto_schema(method='post',
                     request_body=BybitKeyCheckSerializer)
@api_view(['POST'])
def validate_bybit_keys(request):
    serializer = BybitKeyCheckSerializer(data=request.data)
    if serializer.is_valid():
        api_key = serializer.validated_data['api_key']
        api_secret = serializer.validated_data['api_secret']
        is_valid = check_bybit_keys(api_key, api_secret)
        return Response({'is_valid': is_valid}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post',
                     request_body=InviteRequestSerializer)
@api_view(['POST'])
def CheckKyc(request):
    serializer = InviteRequestSerializer(data=request.data)
    if serializer.is_valid():
        KYC = CheckKYC(serializer.validated_data['telegram_id'])
        return Response({'KYC': bool(KYC)})


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


@api_view(['GET'])
def get_user_referrals(request, telegram_id):
    user = get_object_or_404(User, TelegramId=telegram_id)
    referrals = user.referrals.all()
    referred_users = [ref.referred_user for ref in referrals]

    serializer = UserSerializer(referred_users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    # static_response = [
    #     {
    #         "id": "123e4567-e89b-12d3-a456-426614174000",
    #         "TelegramId": 987654321,
    #         "BybitId": "8510122",
    #         "Balance": 250.75,
    #         "RegistrationDate": "2024-10-14T12:30:00Z",
    #         "RegisteredWithReferral": True,
    #         "points": 100
    #     },
    #     {
    #         "id": "223e4567-e89b-12d3-a456-426614174001",
    #         "TelegramId": 123456789,
    #         "BybitId": "4567890",
    #         "Balance": 150.25,
    #         "RegistrationDate": "2024-10-10T09:15:00Z",
    #         "RegisteredWithReferral": True,
    #         "points": 50
    #     }
    # ]
    #
    # return Response(static_response, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post',
                     request_body=FeesRequestSerializer,
                     responses={200: FeesResponseSerializer})
@api_view(['POST'])
def fee_amount(request):
    serializer = FeesRequestSerializer(data=request.data)
    if serializer.is_valid():
        bybit_id = serializer.validated_data['bybit_id']

        registered, traded_volume = bybit_ref(bybit_id)
        traded_volume = traded_volume.get('result').get('takerVol365Day')
        print(registered, traded_volume)
        if registered:
            fees = (float(traded_volume) * 0.001
                    + float(traded_volume) * 0.0003)
            tax = fees * 2
            return JsonResponse({'success': True, 'Fees': fees, 'Tax': tax, 'TradingVolume': float(traded_volume), 'Balance': 24}, status=200)
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


class TaskViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Task.objects.filter(is_active=True)
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]  # Разрешаем запросы без аутентификации

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('telegram_user_id', openapi.IN_QUERY,
                description="Telegram User ID", type=openapi.TYPE_STRING,
                required=True
            )
        ]
    )
    def list(self, request):
        telegram_user_id = request.query_params.get('telegram_user_id')
        if not telegram_user_id:
            return Response({"error": "Telegram User ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        tasks = Task.objects.filter(is_active=True)
        user_tasks = UserTask.objects.filter(telegram_user_id=telegram_user_id)
        completed_task_ids = [user_task.task.id for user_task in user_tasks if user_task.is_completed]

        serialized_tasks = []
        for task in tasks:
            serialized_task = TaskSerializer(task).data
            serialized_task['is_completed'] = task.id in completed_task_ids
            serialized_tasks.append(serialized_task)

        return Response(serialized_tasks)


class CompleteTaskViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'telegram_user_id': openapi.Schema(type=openapi.TYPE_STRING, description='Telegram User ID'),
                'task_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Task ID'),
            },
            required=['telegram_user_id', 'task_id'],
        )
    )
    def create(self, request):
        telegram_user_id = request.data.get('telegram_user_id')
        task_id = request.data.get('task_id')

        if not telegram_user_id:
            return Response({"success": False}, {"error": "Telegram User ID is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not task_id:
            return Response({"success": False},{"error": "Task ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(pk=task_id, is_active=True)
        except Task.DoesNotExist:
            return Response({"success": False, "message": "Task not found or inactive"}, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(TelegramId=telegram_user_id)
        except User.DoesNotExist:
            return Response({"success": False, "message": "User not found"}, status=status.HTTP_200_OK)

        user_task, created = UserTask.objects.get_or_create(telegram_user_id=telegram_user_id, task=task)

        if user_task.is_completed:
            return Response({"success": False}, {"message": "Task already completed"}, status=status.HTTP_400_BAD_REQUEST)

        if not user_task.is_completed:
            user.points += task.reward_points
            user.save()
            user_task.is_completed = True
            user_task.completed_at = timezone.now()
            user_task.save()
            return Response({"success": True},{'status': 'Task completed'}, status=status.HTTP_200_OK)