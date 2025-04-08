from django.urls import path
from .views import RegistrationView, UserListView, UserDetailView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/registration', RegistrationView.as_view(), name='registration'),
    path('api/login', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/users', UserListView.as_view(), name='user_list'),
    path('api/users/<int:pk>', UserDetailView.as_view(), name='user_detail'),
    path('api/logout', LogoutView.as_view(), name='logout'),
]
