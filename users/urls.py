from django.urls import path

from users.views import (
    AccountView,
    RegisterView,
    LoginView,
    VerifyEmailView,
    CheckoutTemplateView,
    UserPasswordResetView,
    WishlistView,
    CartView,
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('account/', AccountView.as_view(), name='account'),
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    path('cart/', CartView.as_view(), name='cart'),
    path('reset-password/', UserPasswordResetView.as_view(), name='reset-password'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
    path('checkout/', CheckoutTemplateView.as_view(), name='checkout'),
]
