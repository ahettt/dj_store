from rest_framework import serializers
from .models import Cart, CartItem
from store.serializers import ProductSerializer # Импортируем сериализатор товаров

class CartItemSerializer(serializers.ModelSerializer):
    # Вкладываем данные о товаре, чтобы React сразу получил картинку и цену
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'created_at']