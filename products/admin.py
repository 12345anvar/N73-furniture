from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from products.models import (
    ProductCategory, ProductTag, ProductColor,
    Manufacture, Product, ProductImage, ProductColorQuantity
)
from shared.admin import MyTranslationOption


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4
    max_num = 4
    min_num = 4
    fields = ['image', 'alt_text', 'is_primary', 'order']


class ProductColorQuantityInline(admin.TabularInline):
    model = ProductColorQuantity
    extra = 1
    min_num = 1
    fields = ['color', 'quantity']


@admin.register(ProductCategory)
class ProductCategoryAdmin(MyTranslationOption):
    list_display = ['id', 'name', 'parent', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active', 'parent', 'created_at']
    list_editable = ['is_active']


@admin.register(ProductTag)
class ProductTagAdmin(MyTranslationOption):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']


@admin.register(ProductColor)
class ProductColorAdmin(MyTranslationOption):
    list_display = ['id', 'name', 'hex_code', 'created_at']
    search_fields = ['name', 'hex_code']
    list_filter = ['created_at']


@admin.register(Manufacture)
class ManufactureAdmin(MyTranslationOption):
    list_display = ['id', 'name', 'country', 'is_active', 'created_at']
    search_fields = ['name', 'country']
    list_filter = ['is_active', 'country', 'created_at']
    list_editable = ['is_active']


@admin.register(Product)
class ProductAdmin(MyTranslationOption):
    list_display = [
        'id', 'name', 'sku', 'price_uzs', 'price_usd', 'price_rub',
        'total_stock', 'status', 'manufacture', 'is_featured', 'is_active', 'created_at'
    ]
    search_fields = ['name', 'sku', 'description', 'short_description']
    list_filter = [
        'status', 'is_featured', 'is_active', 'manufacture',
        'categories', 'tags', 'colors', 'created_at'
    ]
    list_editable = ['is_featured', 'is_active', 'status']
    filter_horizontal = ['categories', 'tags']
    inlines = [ProductColorQuantityInline, ProductImageInline]
    fieldsets = (
        (_("Basic Info"), {
            'fields': ('name', 'sku', 'short_description', 'description', 'image')
        }),
        (_("Pricing (UZS)"), {
            'fields': ('price_uzs', 'discount_price_uzs')
        }),
        (_("Pricing (USD)"), {
            'fields': ('price_usd', 'discount_price_usd')
        }),
        (_("Pricing (RUB)"), {
            'fields': ('price_rub', 'discount_price_rub')
        }),
        (_("Status"), {
            'fields': ('status',)
        }),
        (_("Relations"), {
            'fields': ('manufacture', 'categories', 'tags')
        }),
        (_("Flags"), {
            'fields': ('is_featured', 'is_active')
        }),
    )

    @admin.display(description=_("Total Stock"))
    def total_stock(self, obj):
        return obj.total_stock

