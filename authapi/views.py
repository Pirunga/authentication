from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.viewsets import ModelViewSet

from .models import CustomUser
from .serializers import (
    CustomUserSerializer,
    CustomUserCreateSerializer,
    CustomUserLoginSerializer,
    CustomUserLogoutSerializer
)
from .utils import generate_timestamp


class CustomUserView(ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data
        full_name = validated_data.get('first_name').lower() + validated_data.get('last_name').lower()
        username = ''.join(full_name) + generate_timestamp()

        user = CustomUser.objects.create_user(
            username=username,
            email=validated_data.get('email'),
            first_name=validated_data.get('first_name'),
            last_name=validated_data.get('last_name'),
        )
        user.set_password(request.data.get('password'))
        user.save()

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            user = CustomUser.objects.get(id=user.id)
            serializer = CustomUserSerializer(user)
            return Response(serializer.data)
        
        return Response({
            'error': 'User not authenticated'
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserLoginView(ModelViewSet):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserLoginSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            request,
            username=request.data.get('email'),
            password=request.data.get('password')
        )

        if user:
            token = RefreshToken.for_user(user)
            return Response({
                'token': {
                    'refresh_token': str(token),
                    'access_token': str(token.access_token)
                }
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class UserLogoutView(ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserLogoutSerializer

    def create(self, request, *args, **kwargs):
        try:
            # if request.user.is_authenticated:
            token = RefreshToken(request.data['refresh_token'])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)

        except Exception as e:
            print(e)
            return Response(status=status.HTTP_400_BAD_REQUEST)