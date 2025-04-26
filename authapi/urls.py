from django .urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomUserView, UserLoginView, UserLogoutView


urlpatterns = [
    path('register/', CustomUserView.as_view({'post': 'create'}), name='register'),
    path('me/', CustomUserView.as_view({'get': 'retrieve'}), name='user_me'),
    path('login/', UserLoginView.as_view({'post': 'create'}), name='login'),
    path('logout/', UserLogoutView.as_view({'post': 'create'}), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]