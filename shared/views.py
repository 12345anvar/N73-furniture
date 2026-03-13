from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView, FormView
from shared.forms import ContactForm
from shared.models import Team

class HomeTemplateView(TemplateView):
    template_name = 'shared/home.html'

class ContactFormView(FormView):
    template_name = 'shared/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('shared:contact')

    def form_valid(self, form):
        form.save()
        text = _("Successfully sent to the admin, thanks for your attention.")
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

class AboutTemplateView(TemplateView):
    template_name = 'shared/about-us.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["members"] = Team.objects.filter(is_active=True).order_by("-created_at")