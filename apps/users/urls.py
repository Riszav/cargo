from django.urls import path
from . import views


urlpatterns = [
    path('users/create/', views.UserCreateAPIView.as_view(), name='user-create'),
    path('users/confirm-email/', views.EmailConfirmationAPIView.as_view(), name='email-confirmation'),
    
    path('countries/', views.CountryListAPIView.as_view(), name='country-list'),
    path('users/', views.UserListAPIView.as_view(), name='user-list'),
    path('users/<int:pk>/', views.UserDetailAPIView.as_view(), name='user-detail'),
    path('users/<int:pk>/recipients/', views.UserRecipientListCreateAPIView.as_view(), name='user-recipient-list-create'),
    path('users/recipients/', views.RecipientListAPIView.as_view(), name='recipient-list'),
    path('users/recipients/<int:pk>/', views.RecipientDetailAPIView.as_view(), name='recipient-detail'),
    path('profile/', views.ProfileDetailAPIView.as_view(), name='user-client-detail'),
    path('profile/recipient/', views.ProfileRecipientAPIView.as_view(), name='user-client-recipient'),
    path('profile/recipient/<int:pk>/', views.ProfileRecipientDetailAPIView.as_view(), name='user-client-recipient-detail'),
    path('profile/recipient/<int:pk>/make-main/', views.ProfileRecipientMainAPIView.as_view(), name='user-client-recipient-main'),
    path('users/client/change-password/', views.UserClientChangePasswordAPIView.as_view(), name='user-client-change-password'),
    
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('refresh/', views.UserRefreshAPIView.as_view(), name='user-refresh'),
    path('logout/', views.UserLogoutAPIView.as_view(), name='user-logout'),
]