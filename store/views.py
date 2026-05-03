from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Q
from django.core.paginator import Paginator
from rest_framework import generics
from .serializers import ProductSerializer, CategorySerializer
from thefuzz import fuzz

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'page_obj': page_obj,
        'query': query
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'cart_product_form': cart_product_form
    })

class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        # Берем все доступные товары
        queryset = Product.objects.filter(available=True)

        category_slug = self.request.query_params.get('category')
        search_query = self.request.query_params.get('search')

        # Обычная фильтрация по категории
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        # Умная фильтрация по поиску
        if search_query:
            search_query = search_query.lower()
            matched_ids = []

            for product in queryset:
                name_score = fuzz.token_set_ratio(search_query, product.name.lower())
                desc_score = fuzz.token_set_ratio(search_query, product.description.lower())
                cat_score = fuzz.token_set_ratio(search_query, product.category.name.lower())

                # Если сходство больше 60%, считаем, что товар найден
                if name_score > 60 or desc_score > 60 or cat_score > 60:
                    matched_ids.append(product.id)

            # Оставляем только те товары, ID которых попали в наш список
            queryset = queryset.filter(id__in=matched_ids)

        return queryset


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.filter(available=True)
    serializer_class = ProductSerializer
    lookup_field = 'id'