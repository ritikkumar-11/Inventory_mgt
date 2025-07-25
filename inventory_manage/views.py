from .models import Product
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer, UpdateProductSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema


class UserCreateView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializers = UserSerializer(data = request.data)
        if serializers.is_valid():
            serializers.save()
            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class CreateProductView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10  
        result_page = paginator.paginate_queryset(products, request)
        serializer = ProductSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    @swagger_auto_schema(request_body=ProductSerializer)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"id": serializer.instance.id, "message": "Product Created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ProductUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializers = UpdateProductSerializer(product, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.instance.quantity, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        



    
        
