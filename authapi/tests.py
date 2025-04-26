from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse, resolve
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

@override_settings(
    ROOT_URLCONF='authapi.urls'
)  # exemplo de como isolar settings
class UserTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        
        self.urls = {
            'register': '/register/',
            'login': '/login/',
            'logout': '/logout/',
            'me': '/me/',
        }

        self.user_data = {
            'email': 'test@example.com',
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'strongpassword123'
        }

        self.user = self.create_user(**self.user_data)
        self.access_token, self.refresh_token = self.get_tokens_for_user(self.user)

    def create_user(self, **kwargs):
        """Helper to create a user"""
        return User.objects.create_user(username='usertest', **kwargs)

    def get_tokens_for_user(self, user):
        """Helper to get JWT tokens"""
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token), str(refresh)

    def auth_client(self):
        """Authenticate the client"""
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')

    def test_authenticated_user_detail(self):
        self.auth_client()
        response = self.client.get(self.urls['me'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_user_logout(self):
        self.auth_client()
        response = self.client.post(self.urls['logout'], {'refresh_token': self.refresh_token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)

    def test_user_login(self):
        login_data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(self.urls['login'], login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_unregister_user_login(self):
        login_data = {
            'email': 'unregister@user.com',
            'password': self.user_data['password']
        }
        response = self.client.post(self.urls['login'], login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_registration(self):
        new_user_data = {
            'email': 'new@example.com',
            'first_name': 'Jane',
            'last_name': 'Doe',
            'password': 'strongpassword123'
        }
        response = self.client.post(self.urls['register'], new_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email=new_user_data['email']).exists())

    def test_unauthenticated_user_detail(self):
        response = self.client.get(self.urls['me'])
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_unauthenticated_user_logout(self):
        response = self.client.post(self.urls['logout'], {'refresh_token': 'Not Valid Token'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
