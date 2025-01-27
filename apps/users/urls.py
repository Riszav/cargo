from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),
]