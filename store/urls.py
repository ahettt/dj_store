from django.urls import path
from . import views
from .views import ProductListAPIView

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    path('api/v1/products/', ProductListAPIView.as_view(), name='api_product_list'),
]