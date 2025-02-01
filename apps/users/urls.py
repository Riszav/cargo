from django.urls import path
from . import views


urlpatterns = [
    path('countries/', views.CountryListAPIView.as_view(), name='country-list'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    path('users/client/', views.UserClientDetailAPIView.as_view(), name='user-client-detail'),
    path('users/client/change-password/', views.UserClientChangePasswordAPIView.as_view(), name='user-client-change-password'),
    
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('refresh/', views.UserRefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='user-logout'),
]