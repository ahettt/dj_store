from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    sell_price = serializers.ReadOnlyField(source='get_sell_price')

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'price', 'discount', 'sell_price', 'image', 'available']