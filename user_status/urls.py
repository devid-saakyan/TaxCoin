from django.urls import path
from .views import GetUserStateController, PostUserStateController

urlpatterns = [
    path('state/<int:telegram_id>/', GetUserStateController.as_view(), name='get_user_state'),  # Для GET-запроса
    path('state/', PostUserStateController.as_view(), name='post_user_state'),  # Для POST-запроса
]
