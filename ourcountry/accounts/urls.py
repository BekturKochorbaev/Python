from django.urls import path, include
from .views import (
    RegisterView, CustomLoginView, LogoutView, UserCommentsHistoryAPIView, verify_reset_code,
    custom_password_reset
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('user_comments/', UserCommentsHistoryAPIView.as_view(), name='user_comments'),
    path('password_reset/verify_code/', verify_reset_code, name='verify_reset_code'),
    path('password_reset/', custom_password_reset, name='custom_password_reset'),

]
