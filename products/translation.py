from modeltranslation.translator import register, TranslationOptions

from products.models import (
    ProductCategory, ProductTag, ProductColor,
    Manufacture, Product
)


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProductTag)
class ProductTagTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(ProductColor)
class ProductColorTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Manufacture)
class ManufactureTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'country',)


@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'short_description',)

