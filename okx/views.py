from django.shortcuts import render
from django.http import JsonResponse
from .models import User, Referral
from .utlis import okx_ref, check_okx_keys, CheckKyc
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
from telegramAdmin import is_user_in_channel
from django.utils.timezone import now
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(method='post',
                     request_body=VerifyUserSerializer,
                     responses={200: VerifyUserResponseSerializer})
@api_view(['POST'])
def verify_user(request):
    serializer = VerifyUserSerializer(data=request.data)
    print(serializer)
    if serializer.is_valid():
        telegram_id = serializer.validated_data['telegram_id']
        OKX_id = serializer.validated_data['OKX_id']
        referral_id = serializer.validated_data.get('referral_id')
        nickname = serializer.validated_data.get('nickname')
        firstname = serializer.validated_data.get('firstname')
        lastname = serializer.validated_data.get('lastname')
        photo_url = serializer.validated_data.get('photo_url')
        RegisteredWithReferral = bool(referral_id)

        if referral_id:
            try:
                referral_id = int(referral_id)
            except ValueError:
                return JsonResponse({'error': 'Invalid referral ID'}, status=200)

            referrer = User.objects.filter(TelegramId=referral_id).first()
            if referrer and referrer.referrals.filter(referred_user__TelegramId=telegram_id).exists():
                return JsonResponse({'error': 'Mutual referrals are not allowed'}, status=200)

        registered, traded_volume = okx_ref(OKX_id)
        if registered:
            try:
                user, created = User.objects.update_or_create(
                    TelegramId=telegram_id,
                    defaults={
                        'OKXId': OKX_id,
                        'Balance': traded_volume,
                        'RegisteredWithReferral': RegisteredWithReferral,
                        'nickname': nickname,
                        'firstname': firstname,
                        'lastname': lastname,
                        'photo_url': photo_url,
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
                if 'OKXId' in str(e):
                    error_message = 'OKX ID already exists.'
                elif 'TelegramId' in str(e):
                    error_message = 'Telegram ID already exists.'
                else:
                    error_message = 'A unique constraint failed.'

                return JsonResponse({'error': error_message}, status=400)

        else:
            return JsonResponse({'success': False, 'message': 'User not registered with referral'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


@swagger_auto_schema(method='post',
                     request_body=OKXKeyCheckSerializer)
@api_view(['POST'])
def validate_OKX_keys(request):
    serializer = OKXKeyCheckSerializer(data=request.data)
    if serializer.is_valid():
        api_key = serializer.validated_data['api_key']
        api_secret = serializer.validated_data['api_secret']
        is_valid = check_okx_keys(api_key, api_secret)
        return Response({'is_valid': is_valid}, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post',
                     request_body=InviteRequestSerializer)
@api_view(['POST'])
def CheckKyc(request):
    serializer = InviteRequestSerializer(data=request.data)
    if serializer.is_valid():
        KYC = CheckKyc(serializer.validated_data['telegram_id'])
        return Response({'KYC': bool(KYC)})


@swagger_auto_schema(method='post',
                     request_body=InviteRequestSerializer)
@api_view(['POST'])
def CheckSubscribe(request):
    serializer = InviteRequestSerializer(data=request.data)
    if serializer.is_valid():
        print(serializer.validated_data['telegram_id'])
        subscribed = is_user_in_channel(serializer.validated_data['telegram_id'])
        return Response({'Subscribed': subscribed})


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
    #         "OKXId": "8510122",
    #         "Balance": 250.75,
    #         "RegistrationDate": "2024-10-14T12:30:00Z",
    #         "RegisteredWithReferral": True,
    #         "points": 100
    #     },
    #     {
    #         "id": "223e4567-e89b-12d3-a456-426614174001",
    #         "TelegramId": 123456789,
    #         "OKXId": "4567890",
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
        OKX_id = serializer.validated_data['OKX_id']

        registered, traded_volume = okx_ref(OKX_id)
        traded_volume = traded_volume
        print(registered, traded_volume)
        if registered:
            user = User.objects.filter(OKXId=OKX_id).first()
            if user:
                balance = user.Balance
            else:
                balance = 0
            fees = (float(traded_volume) * 0.001
                    + float(traded_volume) * 0.0003)
            tax = fees * 2

            return JsonResponse({
                'success': True,
                'Fees': fees,
                'Tax': tax,
                'TradingVolume': float(traded_volume),
                'Balance': balance
            }, status=200)
        else:
            return JsonResponse({'success': False, 'error': 'Failed to retrieve data from OKX API'}, status=200)
    else:
        return JsonResponse({'success': False, 'error': 'Invalid input'}, status=200)


@api_view(['GET'])
def get_points(request, telegram_id):
    try:
        user = User.objects.get(TelegramId=telegram_id)
        serializer = UserSerializer(user)
        return Response({"points": serializer.data.get('points')}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_200_OK)


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
        return JsonResponse({'success': False, 'error': 'Invalid input', 'details': serializer.errors}, status=200)


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
            return Response({"error": "Telegram User ID is required"}, status=status.HTTP_200_OK)

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
            return Response({"success": False, "error": "Telegram User ID is required"}, status=status.HTTP_200_OK)
        if not task_id:
            return Response({"success": False,  "error": "Task ID is required"}, status=status.HTTP_200_OK)

        try:
            task = Task.objects.get(pk=task_id, is_active=True)
        except:
            return Response({"success": False, "message": "Task not found or inactive"}, status=status.HTTP_200_OK)

        try:
            user = User.objects.get(TelegramId=telegram_user_id)
        except:
            return Response({"success": False, "message": "User not found"}, status=status.HTTP_200_OK)

        user_task, created = UserTask.objects.get_or_create(telegram_user_id=telegram_user_id, task=task)

        if user_task.is_completed:
            return Response({"success": False, "message": "Task already completed"}, status=status.HTTP_200_OK)

        if not user_task.is_completed:
            user.points += task.reward_points
            user.save()
            user_task.is_completed = True
            user_task.completed_at = timezone.now()
            user_task.save()
            return Response({"success": True,
                             'status': 'Task completed'}, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('TelegramId', openapi.IN_QUERY, description="Telegram User ID", type=openapi.TYPE_INTEGER),
    ], responses={200: UserStateSerializer})
@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'TelegramId': openapi.Schema(type=openapi.TYPE_INTEGER, description="Telegram User ID"),
            'state': openapi.Schema(type=openapi.TYPE_INTEGER, description="New state"),
        },required=['TelegramId', 'state'],
    ),responses={200: UserStateSerializer}
)
@api_view(['GET', 'POST'])
def user_state_view(request):
    if request.method == 'GET':
        telegram_id = request.query_params.get('TelegramId')
        if not telegram_id:
            return Response({'error': 'TelegramId is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user_state = UserState.objects.get(telegram_id=telegram_id)
            serializer = UserStateSerializer(user_state)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except UserState.DoesNotExist:
            return Response({'error': 'User state not found'}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        telegram_id = request.data.get('TelegramId')
        new_state = request.data.get('state')

        if not telegram_id or new_state is None:
            return Response({'error': 'TelegramId and state are required'}, status=status.HTTP_400_BAD_REQUEST)

        user_state, created = UserState.objects.update_or_create(
            telegram_id=telegram_id,
            defaults={'state': new_state, 'updated_at': now()}
        )

        serializer = UserStateSerializer(user_state)
        if created:
            message = "State created successfully"
        else:
            message = "State updated successfully"
        return Response({'message': message, 'data': serializer.data}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_user_wallet(request):
    serializer = UserWalletSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_user_wallet(request, telegram_id):
    try:
        wallet = UserWallet.objects.get(telegram_id=telegram_id)
        serializer = UserWalletSerializer(wallet)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except UserWallet.DoesNotExist:
        return Response({'error': 'Wallet not found for the given telegram_id'}, status=status.HTTP_404_NOT_FOUND)