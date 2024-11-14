from .views import UserView, VerifyTokenView, RegisterUserView
from django.urls import path


app_name = 'user'


urlpatterns = [
    path('login', UserView.as_view(), name='login'),
    path('verify_token', VerifyTokenView.as_view(), name='verify-token'),
    path('register', RegisterUserView.as_view(), name='register-user'),
]