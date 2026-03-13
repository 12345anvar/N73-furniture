from modeltranslation.translator import register, TranslationOptions

from blogs.models import Category, Tag, Author, Blog


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Tag)
class TagTranslationOptions(TranslationOptions):
    fields = ('title',)


@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('full_name', 'about', 'professions',)


@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'short_description', 'long_description',)
