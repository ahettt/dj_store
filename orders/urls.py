from django.urls import path
from . import views
from .views import OrderCreateAPIView

app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    path('history/', views.user_orders, name='user_orders'),
    path('api/v1/create/', OrderCreateAPIView.as_view(), name='api_order_create'),
]