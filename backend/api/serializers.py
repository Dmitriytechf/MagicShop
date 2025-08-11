from django.contrib.auth import get_user_model
from rest_framework import serializers
from djoser.serializers import UserCreateSerializer

from shop.models import Category, Product
from account.models import Profile


User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        many=False,
        slug_field="name",
        queryset=Category.objects.all(),
    )
    
    class Meta:
        model = Product
        fields = ["id", "title", "brand", "image", "category", 
                  "price", "created_at", "update_at"]


class ProductDetailSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    category = serializers.SlugRelatedField(
        many=False,
        slug_field="name",
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "brand", "category", "price",
                  "image", "available", "discount", "created_at", "update_at", "discount"]


class ProfileSerializer(serializers.ModelSerializer):
    # Достаем имя с помощью __str__ метода из модели Profile
    user = serializers.StringRelatedField()

    class Meta:
        model = Profile
        fields = ["user", "avatar"]


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name')
