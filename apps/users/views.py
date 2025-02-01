from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from config.permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from . import models, serializers
from .utils import generate_client_id


class CountryListAPIView(ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer


@extend_schema(tags=['Users'])

class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = models.User.objects.all()
        if self.request.query_params.get('id'):
            queryset = queryset.filter(id=self.request.query_params.get('id'))
        if self.request.query_params.get('email'):
            queryset = queryset.filter(email=self.request.query_params.get('email'))
        if self.request.query_params.get('phone_number'):
            queryset = queryset.filter(phone_number=self.request.query_params.get('phone_number'))
        if self.request.query_params.get('resipient'):
            queryset = queryset.filter(resipient=self.request.query_params.get('resipient'))
        return queryset


@extend_schema(tags=['Users'])
class UserCreateAPIView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.User.objects.create_user(**serializer.validated_data)
        password = serializer.validated_data['password']
        user.date_login = timezone.now()
        
        client_id = generate_client_id()
        while models.User.objects.filter(client_id=client_id).exists():
            client_id = generate_client_id()
        user.client_id = client_id
        user.save()
        
        refresh = RefreshToken.for_user(user)
        refresh.payload.update({
            'user_id': user.id,
            'user_email': user.email,
            'user_phone_number': user.phone_number,
        })
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'is_admin': user.is_admin,
        }, status=status.HTTP_201_CREATED)
        

class UserDetailAPIView(RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
    

class UserClientDetailAPIView(RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return models.User.objects.get(id=self.request.user.id)
    

class UserClientChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.UserClientChangePasswordSerializer
    
    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        if not old_password or not new_password or not confirm_password:
            return Response(data='Неверные данные', status=status.HTTP_400_BAD_REQUEST)
        if not request.user.check_password(old_password):
            return Response(data='Неверный пароль', status=status.HTTP_400_BAD_REQUEST)
        if new_password != confirm_password:
            return Response(data='Пароли не совпадают', status=status.HTTP_400_BAD_REQUEST)
        request.user.set_password(new_password)
        request.user.save()
        return Response(data='Пароль успешно изменен', status=status.HTTP_200_OK)
    

@extend_schema(tags=['Auth'])
class UserLoginAPIView(APIView):
    serializer_class = serializers.UserLoginSerializer
    
    @extend_schema(
        description='''Введите данные для входа в систему''',
        request=serializers.UserLoginSerializer,
        responses=serializers.UserLoginSerializer
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            user = models.User.objects.get(email=serializer.validated_data['username'])
        except models.User.DoesNotExist:
            try:
                user = models.User.objects.get(phone_number=serializer.validated_data['username'])
            except models.User.DoesNotExist:
                return Response(data='Пользователь с таким email или номером телефона не найден', status=status.HTTP_204_NO_CONTENT)
        if not user.is_active:
            return Response(data='Пользователь не активен', status=status.HTTP_204_NO_CONTENT)
        if not user.check_password(serializer.validated_data['password']):
            return Response(data='Неверный пароль', status=status.HTTP_204_NO_CONTENT)
        user.date_login = timezone.now()
        user.save()
        refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
        refresh.payload.update({  # Полезная информация в самом токене
            'user_id': user.id,
            'user_email': user.email,
            'user_phone_number': user.phone_number,
        })
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),  # Отправка на клиент
            'is_admin': user.is_admin,
        }, status=status.HTTP_200_OK)

@extend_schema(tags=['Auth'])
class UserRefreshAPIView(TokenRefreshView):
    serializer_class = serializers.UserRefreshSerializer


@extend_schema(tags=['Auth'])
class UserLogoutAPIView(TokenBlacklistView):
    serializer_class = serializers.UserLogoutSerializer
