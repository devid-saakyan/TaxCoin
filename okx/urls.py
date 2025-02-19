from django.urls import path
from .views import *

urlpatterns = [
    path('verify/', verify_user, name='verify_user'),
    path('check_api_keys/', validate_OKX_keys, name='api keys check'),
    path('users/', list_users, name='list_users'),
    path('users/<uuid:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('users/telegram/<int:telegram_id>/', get_user_by_telegram_id, name='get_user_by_telegram_id'),
    path('users/<uuid:user_id>/delete/', delete_user_by_id, name='delete_user_by_id'),
    path('fees/', fee_amount, name='fee_amount'),
    path('tax_balance/<int:telegram_id>/', get_points, name='tax_balance'),
    path('invitelink/', get_invitation_link, name='get_invitation_link'),
    path('tasks/', TaskViewSet.as_view({'get': 'list'}), name='get_tasks'),
    path('complete_task/', CompleteTaskViewSet.as_view({'post': 'create'}), name='complete_task'),
    path('wallet/create/', create_user_wallet, name='create_user_wallet'),
    path('wallet/<int:telegram_id>/', get_user_wallet, name='get_user_wallet'),
    path('referrals/<int:telegram_id>/', get_user_referrals, name='referrals'),
    path('KYC/', check_kyc_view, name='referrals'),
    path('Subscribed/', CheckSubscribe, name='Subscribe'),
    path('CheckState/', user_state_view, name='user_state_view'),
]