import threading
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import TemplateView, FormView

from users.forms import CustomUserCreationForm, CustomAuthenticationForm
from users.utils import email_verification_token

User = get_user_model()

class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        user.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = email_verification_token.make_token(user)

        link = self.request.build_absolute_uri(
            reverse('users:verify-email', kwargs={'uidb64': uid, 'token': token})
        )

        thread = threading.Thread(target=send_mail, kwargs={
            'subject': 'Verify your email',
            'message': f'Click to verify your account: {link}',
            'from_email': 'noreply@yourapp.com',
            'recipient_list': [user.email],
        })
        thread.start()

        text = _("We sent a confirmation link to your email, please verify it")
        messages.success(self.request, text)

        return super().form_valid(form)

    def form_invalid(self, form):
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field}: {error}")

        error_text = " | ".join(errors)
        messages.error(self.request, error_text)

        return super().form_invalid(form)
class VerifyEmailView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, User.DoesNotExist):
            user = None

        if user and email_verification_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect('shared:home')

        messages.error(request, _("Something went wrong, please try again later"))
        return render(request, 'users/login.html')

class LoginView(FormView):
    template_name = "users/login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("shared:home")

    def form_valid(self, form):
        user = form.cleaned_data["user"]
        login(self.request, user)
        return super().form_valid(form)

    def form_invalid(self, form):
        errors = []
        for field, field_errors in form.errors.items():
            for error in field_errors:
                errors.append(f"{field}: {error}")

        error_text = " | ".join(errors)
        messages.error(self.request, error_text)

        return super().form_invalid(form)

class AccountTemplateView(TemplateView):
    template_name = 'users/account.html'

class ResetPasswordTemplateView(TemplateView):
    template_name = 'users/reset-password.html'