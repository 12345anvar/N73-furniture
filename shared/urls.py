from django.urls import path

from shared.views import HomeTemplateView, AboutTemplateView, ContactFormView

app_name = 'shared'

urlpatterns = [
    path('', HomeTemplateView.as_view(), name='home'),
    path('about/', AboutTemplateView.as_view(), name='about'),
    path('contact/', ContactFormView.as_view(), name='contact')
]
