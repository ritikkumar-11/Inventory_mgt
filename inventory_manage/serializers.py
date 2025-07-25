from rest_framework import serializers
from .models import User, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User(username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'name',
            'type',
            'sku',
            'image_url',
            'description',
            'quantity',
            'price',
        ]
    def get_name(self, request, *args, **kwargs):
        print(request.name, self.name)
        return request.name
    def get_type(self, request):
        return request.type

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity should be greater that 0")
        return value
    
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price should be > 0")
        return value
    

class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['quantity']

    def validate_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Quantity should be greater that 0")
        return value
    
    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance
    




        