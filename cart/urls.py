from django.urls import path
from .views import CartAPIView

app_name = 'cart'

urlpatterns = [
    path('api/v1/', CartAPIView.as_view(), name='api_cart'),
]