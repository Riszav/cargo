from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from config.permissions import IsAdmin
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers


class CountryListAPIView(ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer


class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdmin]
    

class UserCreateAPIView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = models.User.objects.create_user(
            email=serializer.validated_data['email'],
            phone_number=serializer.validated_data['phone_number'],
            password=serializer.validated_data['password'],
            last_name=serializer.validated_data['last_name'],
            first_name=serializer.validated_data['first_name'],
            country=serializer.validated_data['country'],
            address=serializer.validated_data['address'],
        )
        password = serializer.validated_data['password']
        # user = models.User.objects.get(id=self.data['id'])
        # user.set_password(password)
        # user.is_active = True
        # user.save()
        refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
        refresh.payload.update({  # Полезная информация в самом токене
            'user_id': user.id,
        })
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),  # Отправка на клиент
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
        refresh = RefreshToken.for_user(user)  # Создание Refesh и Access
        refresh.payload.update({  # Полезная информация в самом токене
            'user_id': user.id,
            'user_email': user.email,
            'user_phone_number': user.phone_number,
        })
        return Response(data={
            'refresh': str(refresh),
            'access': str(refresh.access_token),  # Отправка на клиент
        }, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Auth'])
class UserRefreshAPIView(TokenRefreshView):
    serializer_class = serializers.UserRefreshSerializer


@extend_schema(tags=['Auth'])
class UserLogoutAPIView(TokenBlacklistView):
    serializer_class = serializers.UserLogoutSerializer
