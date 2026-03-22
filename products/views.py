from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView

from products.models import Product, ProductCategory, ProductTag, ProductColor, Manufacture, ProductReview


class ProductListView(ListView):
    model = Product
    template_name = 'products/products-list.html'
    context_object_name = 'products'

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True)

        manufacture = self.request.GET.get('manufacture')
        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        color = self.request.GET.get('color')
        q = self.request.GET.get('q')
        ordering = self.request.GET.get('ordering')
        if q:
            queryset = queryset.filter(Q(name__icontains=q))

        if manufacture:
            queryset = queryset.filter(manufacture__id=int(manufacture))
        if category:
            queryset = queryset.filter(categories__id=int(category))
        if tag:
            queryset = queryset.filter(tags__id=int(tag))
        if color:
            queryset = queryset.filter(colors__id=int(color))

        if ordering in ['name', '-name', 'price_uzs', '-price_uzs']:
            queryset = queryset.order_by(ordering)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['tags'] = ProductTag.objects.all()
        context['colors'] = ProductColor.objects.all()
        context['manufactures'] = Manufacture.objects.filter(is_active=True)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product-detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()

        rating = request.POST.get('rating')
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        comment = request.POST.get('comment', '').strip()

        if str(rating).isdigit() and name and comment:
            rating_value = int(rating)
            if 1 <= rating_value <= 5:
                ProductReview.objects.create(
                    product=self.object,
                    name=name,
                    email=email,
                    rating=rating_value,
                    comment=comment,
                )

        return redirect(f"{reverse_lazy('products:detail', kwargs={'pk': self.object.pk})}#review")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object
        cart = self.request.session.get('cart', [])
        wishlist = self.request.session.get('wishlist', [])
        product_cart_meta = self.request.session.get('cart_item_meta', {}).get(str(product.pk), {})
        color_entries = product_cart_meta.get('colors', {})
        color_options = list(product.color_quantities.select_related('color').order_by('-quantity', 'id'))
        default_color_quantity = color_options[0] if color_options else None

        selected_color_id = self.request.GET.get('color')
        if selected_color_id and not str(selected_color_id).isdigit():
            selected_color_id = None

        if selected_color_id is None and default_color_quantity:
            selected_color_id = default_color_quantity.color_id

        selected_color_key = str(selected_color_id) if selected_color_id is not None else 'default'
        selected_color_meta = color_entries.get(selected_color_key, {})
        reviews = product.reviews.filter(is_active=True)

        for color_option in color_options:
            color_meta = color_entries.get(str(color_option.color_id), {})
            color_option.cart_quantity = color_meta.get('quantity', 0)
            color_option.in_cart = str(color_option.color_id) in color_entries
            color_option.display_stock = max(color_option.quantity - color_option.cart_quantity, 0)

        related_products = Product.objects.filter(
            is_active=True,
            categories__in=product.categories.all()
        ).exclude(pk=product.pk).distinct()[:3]

        if related_products.count() < 3:
            extra_products = Product.objects.filter(
                is_active=True
            ).exclude(
                pk__in=[product.pk, *related_products.values_list('pk', flat=True)]
            )[:3 - related_products.count()]
            related_products = list(related_products) + list(extra_products)

        context['categories'] = ProductCategory.objects.filter(is_active=True)
        context['tags'] = ProductTag.objects.all()
        context['featured_products'] = Product.objects.filter(
            is_active=True
        ).exclude(pk=product.pk).order_by('-is_featured', '-created_at')[:3]
        context['related_products'] = related_products
        context['wishlist'] = wishlist
        context['cart'] = cart
        context['selected_color_id'] = selected_color_id
        context['color_options'] = color_options
        context['cart_item_meta'] = product_cart_meta
        context['selected_color_cart_quantity'] = selected_color_meta.get('quantity', 1)
        context['selected_color_in_cart'] = selected_color_key in color_entries
        context['selected_color_key'] = selected_color_key
        context['selected_color_stock'] = next(
            (color_option.display_stock for color_option in color_options if str(color_option.color_id) == str(selected_color_id)),
            product.total_stock
        )
        context['reviews'] = reviews
        context['review_count'] = reviews.count()
        context['is_in_wishlist'] = product.pk in wishlist
        context['is_in_cart'] = product.pk in cart
        return context


def add_or_remove_from_cart(request, pk):
    cart = request.session.get('cart', [])
    cart_item_meta = request.session.get('cart_item_meta', {})
    existing_item = cart_item_meta.get(str(pk), {})
    color_entries = existing_item.get('colors', {})
    product = Product.objects.filter(pk=pk, is_active=True).first()

    try:
        quantity = max(1, int(request.POST.get('qty', request.GET.get('qty', 1))))
    except (TypeError, ValueError):
        quantity = 1

    color = request.POST.get('color') or request.GET.get('color')
    if (not color or not str(color).isdigit()) and product:
        default_color_quantity = product.color_quantities.select_related('color').order_by('-quantity', 'id').first()
        color = default_color_quantity.color_id if default_color_quantity else None

    color_key = str(color) if color is not None else 'default'
    existing_color_item = color_entries.get(color_key, {})

    existing_quantity = existing_color_item.get("quantity")

    if pk in cart and existing_quantity == quantity:
        color_entries.pop(color_key, None)
    else:
        if pk not in cart:
            cart.append(pk)
        color_entries[color_key] = {
            "quantity": quantity,
            "color": int(color) if color and str(color).isdigit() else None,
        }

    if color_entries:
        cart_item_meta[str(pk)] = {
            "selected_color": int(color) if color and str(color).isdigit() else None,
            "colors": color_entries,
        }
    else:
        cart_item_meta.pop(str(pk), None)
        if pk in cart:
            cart.remove(pk)

    request.session['cart'] = cart
    request.session['cart_item_meta'] = cart_item_meta
    next_url = request.GET.get('next', reverse_lazy('products:list'))
    return redirect(next_url)


def add_or_remove_from_wishlist(request, pk):
    wishlist = request.session.get('wishlist', [])

    if pk in wishlist:
        wishlist.remove(pk)
    else:
        wishlist.append(pk)

    request.session['wishlist'] = wishlist
    next_url = request.GET.get('next', reverse_lazy('products:list'))
    return redirect(next_url)
