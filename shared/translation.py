from modeltranslation.translator import register, TranslationOptions

from shared.models import Team


@register(Team)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('full_name', 'position', 'info',)
