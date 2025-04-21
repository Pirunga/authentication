from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')

class CustomUserCreateSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password1', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError("Passwords do not match")
        
        password = attrs['password1']
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long")

        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError("Password must contain at least one digit")

        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError("Password must contain at least one letter")

        if not any(char in '!@#$%^&*()_+' for char in password):
            raise serializers.ValidationError("Password must contain at least one special character")

        return attrs
    
    def create(self, validated_data):
        password = validated_data.pop('password1')
        validated_data.pop('password2')

        validated_data['username'] = validated_data.get('first_name') + validated_data.get('last_name') + generate_timestamp()

        return CustomUser.objects.create_user(**validated_data, password=password)


class CustomUserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user

        raise serializers.ValidationError("Invalid credentials")