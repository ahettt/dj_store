from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
]