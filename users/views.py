import threading
from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordResetForm
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

class AccountView(LoginRequiredMixin, TemplateView):
    template_name = 'users/account.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        field_candidates = [
            ("My Name", lambda obj: obj.get_full_name() or getattr(obj, "username", "") or getattr(obj, "email", "")),
            ("Username", "username"),
            ("Email", "email"),
            ("First Name", "first_name"),
            ("Last Name", "last_name"),
            ("Company", "company"),
            ("Address", "address"),
            ("City", "city"),
            ("Postal/Zip Code", "zip_code"),
            ("Postal/Zip Code", "postal_code"),
            ("Phone", "phone"),
            ("Phone", "phone_number"),
            ("Country", "country"),
        ]

        details = []
        added_labels = set()

        for label, source in field_candidates:
            if callable(source):
                value = source(user)
            else:
                if not hasattr(user, source):
                    continue
                value = getattr(user, source)

            if value in ("", None):
                continue
            if label in added_labels:
                continue

            details.append({
                "label": label,
                "value": value,
            })
            added_labels.add(label)

        if not details:
            details.append({
                "label": "Username",
                "value": getattr(user, "username", "-") or "-",
            })

        context["account_details"] = details
        return context

class UserPasswordResetView(FormView):
    template_name = 'users/reset-password.html'
    form_class = PasswordResetForm
    success_url = reverse_lazy('users:reset-password')

    def form_valid(self, form):
        messages.success(self.request, _("If this email exists, a reset link was sent successfully"))
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, _("Please enter a valid email address"))
        return super().form_invalid(form)

class CheckoutTemplateView(TemplateView):
    template_name = 'products/checkout.html'


class WishlistView(LoginRequiredMixin, TemplateView):
    template_name = 'products/wishlist.html'
    login_url = reverse_lazy('users:login')


class CartView(TemplateView):
    template_name = 'products/cart.html'
