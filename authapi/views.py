from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken


from .serializers import CustomUserSerializer, CustomUserCreateSerializer, CustomUserLoginSerializer

# Create your views here.

class UserRegistrationView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserCreateSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        token = RefreshToken.for_user(user)
        data = serializer.data
        data['token'] = {
            'refresh': str(token),
            'access': str(token.access_token)
        }
        # Handle user registration logic here
        return Response(data, status=status.HTTP_201_CREATED)


class UserLoginView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = CustomUserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['token']= {
            'token': {
                'refresh': str(token),
                'access': str(token.access_token)
            }
        }
        return Response(data, status=status.HTTP_200_OK)
    

class UserLogoutView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)