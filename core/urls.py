"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = []
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('blogs/', include('blogs.urls', namespace='blogs')),
    path('products/', include('products.urls', namespace='products')),
    path('users/', include('users.urls', namespace='users')),
    path('cart.html', RedirectView.as_view(pattern_name='users:cart', permanent=False)),
    path('wishlist.html', RedirectView.as_view(pattern_name='users:wishlist', permanent=False)),
    path('checkout.html', RedirectView.as_view(pattern_name='users:checkout', permanent=False)),
    path('users/cart/checkout.html', RedirectView.as_view(pattern_name='users:checkout', permanent=False)),
    path('users/checkout/wishlist.html', RedirectView.as_view(pattern_name='users:wishlist', permanent=False)),
    path('', include('shared.urls', namespace='shared')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
