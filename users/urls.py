from django.urls import path

from users.views import AccountTemplateView, ResetPasswordTemplateView, RegisterView, LoginView, VerifyEmailView

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountTemplateView.as_view(), name='account'),
    path('reset-password/', ResetPasswordTemplateView.as_view(), name='reset-password'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
]
