from django.urls import path
from .views import *

urlpatterns = [
    path('verify/', verify_user, name='verify_user'),
    path('users/', list_users, name='list_users'),
    path('users/<uuid:user_id>/', get_user_by_id, name='get_user_by_id'),
    path('users/telegram/<int:telegram_id>/', get_user_by_telegram_id, name='get_user_by_telegram_id'),
    path('users/<uuid:user_id>/delete/', delete_user_by_id, name='delete_user_by_id'),
    path('fees/', fee_amount, name='fee_amount'),
    path('invitelink/', get_invitation_link, name='get_invitation_link'),
]