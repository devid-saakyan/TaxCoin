from django.urls import path
from .views import GetUserStateController, PostUserStateController, AddOrUpdateAPIKeyView, CheckAPIKeyView

urlpatterns = [
    path('state/<int:telegram_id>/', GetUserStateController.as_view(), name='get_user_state'),
    path('state/', PostUserStateController.as_view(), name='post_user_state'),
    path('api_keys/add/', AddOrUpdateAPIKeyView.as_view(), name='add-api-keys'),
    path('api_keys/check/', CheckAPIKeyView.as_view(), name='check-api-keys'),
]
