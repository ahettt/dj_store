from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404
from store.models import Product
from .models import Cart, CartItem
from .serializers import CartSerializer


class CartAPIView(APIView):
    # Доступ разрешен только авторизованным пользователям
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        # Ищем корзину пользователя. Если её еще нет — создаем пустую.
        cart, created = Cart.objects.get_or_create(user=user)
        return cart

    def get(self, request):
        """Получить текущую корзину"""
        cart = self.get_cart(request.user)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def post(self, request):
        """Добавить товар в корзину или увеличить его количество"""
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')
        quantity = int(request.data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id)

        # Проверяем, есть ли уже этот товар в корзине
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            # Если товар уже был, просто прибавляем количество
            cart_item.quantity += quantity
            cart_item.save()
        else:
            # Если товара не было, устанавливаем переданное количество
            cart_item.quantity = quantity
            cart_item.save()

        # Возвращаем обновленную корзину
        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        """Удалить товар из корзины или очистить её полностью"""
        cart = self.get_cart(request.user)
        product_id = request.data.get('product_id')

        if product_id:
            # Если передали ID товара — удаляем только его
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        else:
            # Если ID не передали — очищаем всю корзину
            cart.items.all().delete()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_200_OK)