from django.contrib import admin
from modeltranslation.admin import TranslationAdmin

from shared.models import Contact, Team


class MyTranslationOption(TranslationAdmin):
    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'is_read', 'created_at']
    search_fields = ['full_name', 'email', 'subject', 'message']
    list_filter = ['is_read', 'created_at']


@admin.register(Team)
class ContactAdmin(MyTranslationOption):
    list_display = ['id', 'full_name', 'position', 'is_active', 'created_at']
    search_fields = ['full_name', 'position', 'info']
    list_filter = ['is_active', 'created_at']
