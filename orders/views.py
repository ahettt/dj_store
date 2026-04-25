from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from store.models import Product
from .models import Order


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)

            if request.user.is_authenticated:
                order.user = request.user

            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])

            cart.clear()
            return render(request, 'orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/create.html', {'cart': cart, 'form': form})

@login_required
def user_orders(request):
    orders = request.user.order_set.all().order_by('-created')
    return render(request, 'orders/user_orders.html', {'orders': orders})


class OrderCreateAPIView(APIView):
    def post(self, request):
        data = request.data
        try:
            # Создаем запись о заказе (данные покупателя)
            order = Order.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                address=data.get('address'),
                postal_code=data.get('postal_code'),
                city=data.get('city')
            )

            # Привязываем пользователя, если он авторизован
            if request.user.is_authenticated:
                order.user = request.user
                order.save()

            # Перебираем товары из корзины и сохраняем их в OrderItem
            items = data.get('items', [])
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    price=item['price'],
                    quantity=item['quantity']
                )

            # Возвращаем успешный ответ с номером заказа
            return Response(
                {'order_id': order.id, 'message': 'Заказ успешно создан'},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            # Если что-то пошло не так
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)