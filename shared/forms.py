from django import forms

from shared.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def clean_message(self):
        message = self.cleaned_data.get('message')
        if 'hello' in message.lower():
            raise forms.ValidationError("Hello can not be inside message")
        return message
