from .models import CustomUser
from .utils import generate_timestamp

from django.contrib.auth import authenticate
from rest_framework import serializers
import re


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')


class CustomUserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False)
    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'password', 'username')
        extra_kwargs = {'password': {'write_only': True}}


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class CustomUserLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
