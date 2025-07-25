from .views import UserCreateView, CreateProductView, ProductUpdateView
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
urlpatterns = [
    path('register/', UserCreateView.as_view(), name='create_user'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('products/', CreateProductView.as_view(), name="create_product"),
    path('products/<int:pk>/quantity/', ProductUpdateView.as_view(), name="update_products"),
]