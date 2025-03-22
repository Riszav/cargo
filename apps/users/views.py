from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from config.permissions import *
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils import timezone
from rest_framework import status
from . import models, serializers
from django.db.models import Q
from datetime import timedelta


@extend_schema(tags=['Countries'])
@extend_schema_view(get=extend_schema(summary='СПИСОК ВСЕХ СТРАН'))
class CountryListAPIView(ListAPIView):
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer


@extend_schema(tags=['Users'])
@extend_schema_view(get=extend_schema(summary='СПИСОК ВСЕХ ПОЛЬЗОВАТЕЛЕЙ С ФИЛЬТРОМ'))
class UserListAPIView(ListAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminOrManager]
    
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


@extend_schema(tags=['Users create'])
@extend_schema_view(post=extend_schema(summary='ПРОВЕРКА КОДА ПОДТВЕРЖДЕНИЯ ПОЧТЫ'))
class EmailConfirmationAPIView(APIView):
    serializer_class = serializers.EmailConfirmationSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if models.User.objects.filter(email=email).exists():
            return Response(data='Пользователь с такой почтой уже существует', status=status.HTTP_400_BAD_REQUEST)
        models.ConfirmationCode.objects.filter(email=email).delete()
        models.ConfirmationCode.objects.create(email=email)
        return Response(data='Код подтверждения почты отправлен на почту', status=status.HTTP_200_OK)


@extend_schema(tags=['Users create'])
@extend_schema_view(post=extend_schema(summary='СОЗДАНИЕ ПОЛЬЗОВАТЕЛЯ'))
class UserCreateAPIView(CreateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserCreateSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        if not models.ConfirmationCode.objects.filter(email=serializer.validated_data['email'], code=serializer.validated_data['code']).exclude(
            created_at__gt=timezone.now() - timedelta(minutes=60)).exists():
            return Response(data='Код подтверждения почты недействителен', status=status.HTTP_400_BAD_REQUEST)
        
        serializer.validated_data.pop('code')
        country_id = serializer.validated_data.pop('country_id')
        country = models.Country.objects.get(id=country_id)
        
        address = serializer.validated_data.pop('address')
        passport_image_1 = serializer.validated_data.pop('passport_image_1')
        passport_image_2 = serializer.validated_data.pop('passport_image_2')
        # inn = serializer.validated_data.pop('inn')
        # passport_number = serializer.validated_data.pop('passport_number')
        # passport_date = serializer.validated_data.pop('passport_date')
        # passport_place = serializer.validated_data.pop('passport_place')
        
        user = models.User.objects.create_user(country=country, **serializer.validated_data)
        password = serializer.validated_data['password']
        user.date_login = timezone.now()
        user.save()
        user.set_password(password)
        
        recipient = models.Recipient.objects.create(user=user, country=country, address=address, passport_image_1=passport_image_1, passport_image_2=passport_image_2, main_recipient=True)
        
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
            'is_manager': user.is_manager,
        }, status=status.HTTP_201_CREATED)
        

@extend_schema(tags=['Users'])
@extend_schema_view(get=extend_schema(summary='СПИСОК ВСЕХ ПОЛУЧАТЕЛЕЙ С ФИЛЬТРОМ'))
class RecipientListAPIView(ListAPIView):
    queryset = models.Recipient.objects.all().order_by('-created_at')
    serializer_class = serializers.RecipientSerializer
    permission_classes = [IsAdminOrManager]
    
    def get_queryset(self):
        queryset = models.Recipient.objects.all().order_by('-created_at')
        if self.request.query_params.get('status_recipient'):
            queryset = queryset.filter(status_recipient=self.request.query_params.get('status_recipient'))
        if self.request.query_params.get('full_name'):
            full_name = self.request.query_params.get('full_name').split()
            query = Q()
            for part in full_name:
                query &= (Q(last_name__icontains=part) | Q(first_name__icontains=part))
            queryset = queryset.filter(query)
        if self.request.query_params.get('user_id'):
            queryset = queryset.filter(user_id=self.request.query_params.get('user_id'))
        return queryset


@extend_schema(tags=['Users'])
@extend_schema_view(get=extend_schema(summary='ДЕТАЛИ ПОЛУЧАТЕЛЯ'))
class RecipientDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Recipient.objects.all()
    serializer_class = serializers.RecipientSerializer
    permission_classes = [IsAdminOrManager]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        country_id = serializer.validated_data.pop('country_id', None)
        if country_id:
            country = models.Country.objects.get(id=country_id)
            serializer.save(country=country)
        return serializer.save()
    

@extend_schema(tags=['Users'])
@extend_schema_view(
    get=extend_schema(summary='СПИСОК ВСЕХ ПОЛУЧАТЕЛЕЙ ПОЛЬЗОВАТЕЛЯ'),
    post=extend_schema(summary='СОЗДАНИЕ ПОЛУЧАТЕЛЯ ПОЛЬЗОВАТЕЛЯ')
)
class UserRecipientListCreateAPIView(ListCreateAPIView):
    queryset = models.Recipient.objects.all()
    serializer_class = serializers.RecipientSerializer
    permission_classes = [IsAdminOrManager]

    def get_queryset(self):
        return models.Recipient.objects.filter(user_id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        user = models.User.objects.get(id=self.kwargs['pk'])
        country = models.Country.objects.get(id=self.request.data['country_id'])
        serializer.save(user=user, country=country)
    

@extend_schema(tags=['Users'])
@extend_schema_view(
    get=extend_schema(summary='ПРОСМОТР ПОЛЬЗОВАТЕЛЯ'),
    put=extend_schema(summary='ИЗМЕНЕНИЕ ПОЛЬЗОВАТЕЛЯ'),
    patch=extend_schema(summary='ЧАСТИЧНОЕ ИЗМЕНЕНИЕ ПОЛЬЗОВАТЕЛЯ'),
    delete=extend_schema(summary='УДАЛЕНИЕ ПОЛЬЗОВАТЕЛЯ')
)
class UserDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'pk'
    
    def perform_update(self, serializer):
        country_id = serializer.validated_data.pop('country_id', None)
        if country_id:
            country = models.Country.objects.get(id=country_id)
            serializer.save(country=country)
        return serializer.save()


@extend_schema(tags=['Profile'])
@extend_schema_view(
    get=extend_schema(summary='ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ'),
    put=extend_schema(summary='ИЗМЕНЕНИЕ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ'),
    patch=extend_schema(summary='ЧАСТИЧНОЕ ИЗМЕНЕНИЕ ПРОФИЛЯ ПОЛЬЗОВАТЕЛЯ')
)
class ProfileDetailAPIView(RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return models.User.objects.get(id=self.request.user.id)
    

@extend_schema(tags=['Profile'])
@extend_schema_view(
    get=extend_schema(summary='СПИСОК ВСЕХ ПОЛУЧАТЕЛЕЙ ПОЛЬЗОВАТЕЛЯ'),
    post=extend_schema(summary='СОЗДАНИЕ ПОЛУЧАТЕЛЯ ПОЛЬЗОВАТЕЛЯ')
)
class ProfileRecipientAPIView(ListCreateAPIView):
    queryset = models.Recipient.objects.all()
    serializer_class = serializers.RecipientUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return models.Recipient.objects.filter(user=self.request.user) # .order_by('-main_recipient', '-created_at')
    
    def perform_create(self, serializer):
        user = self.request.user
        country = models.Country.objects.get(id=serializer.validated_data['country_id'])
        recipient = models.Recipient.objects.create(user=user, country=country, **serializer.validated_data)
        return recipient


@extend_schema(tags=['Profile'])
@extend_schema_view(
    get=extend_schema(summary='ПОЛУЧАТЕЛЬ ПОЛЬЗОВАТЕЛЯ'),
    put=extend_schema(summary='ИЗМЕНЕНИЕ ПОЛУЧАТЕЛЯ ПОЛЬЗОВАТЕЛЯ'),
    patch=extend_schema(summary='ЧАСТИЧНОЕ ИЗМЕНЕНИЕ ПОЛУЧАТЕЛЯ ПОЛЬЗОВАТЕЛЯ'),
    delete=extend_schema(summary='УДАЛЕНИЕ ПОЛУЧАТЕЛЯ ПОЛЬЗОВАТЕЛЯ')
)
class ProfileRecipientDetailAPIView(RetrieveUpdateDestroyAPIView):
    queryset = models.Recipient.objects.all()
    serializer_class = serializers.RecipientUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def get_object(self):
        return self.queryset.get(user=self.request.user, id=self.kwargs['pk'])
    
    def perform_create(self, serializer):
        user = self.context['request'].user
        country = models.Country.objects.get(id=serializer.validated_data['country_id'])
        recipient = models.Recipient.objects.create(user=user, country=country, **serializer.validated_data)
        return recipient
    
    def perform_update(self, serializer):
        if self.get_object().status_recipient != 'Отклонен':
            raise ValidationError('Статус получателя не может быть изменен')
        return super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        if instance.status_recipient != 'Отклонен':
            raise ValidationError('Получатель не может быть удален')
        return super().perform_destroy(instance)
     

@extend_schema(tags=['Profile'])
@extend_schema_view(get=extend_schema(summary='СДЕЛАТЬ ПОЛУЧАТЕЛЕМ ОСНОВНЫМ'))
class ProfileRecipientMainAPIView(APIView):
    queryset = models.Recipient.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'
    
    def post(self, request, pk):
        try:
            recipient = self.queryset.get(user=request.user, id=pk)
        except models.Recipient.DoesNotExist:
            return Response(data='Получатель не найден', status=status.HTTP_404_NOT_FOUND)
        if recipient.status_recipient == 'Подтвержден':
            recipient.main_recipient = True
            recipient.save()
            return Response(data='Получатель сделан основным', status=status.HTTP_200_OK)
        return Response(data='Получатель не может быть сделан основным', status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Users Utils'])
@extend_schema_view(post=extend_schema(summary='СМЕНА ПАРОЛЯ ПОЛЬЗОВАТЕЛЯ'))
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
    

@extend_schema(tags=['Users Utils'])
@extend_schema_view(post=extend_schema(summary='ЗАБЫЛИ ПАРОЛЬ (ПОДТВЕРДИТЬ ПОЧТУ)'))
class UserClientForgotPasswordAPIView(APIView):
    serializer_class = serializers.EmailConfirmationSerializer
   
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        models.ConfirmationCode.objects.create(email=email)
        return Response(data='Код подтверждения почты отправлен на почту', status=status.HTTP_200_OK)
    

@extend_schema(tags=['Users Utils'])
@extend_schema_view(post=extend_schema(summary='ЗАБЫЛИ ПАРОЛЬ (ПОДТВЕРДИТЬ КОД)'))
class UserClientForgotPasswordConfirmAPIView(APIView):
    serializer_class = serializers.EmailConfirmationConfirmSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        if not models.ConfirmationCode.objects.filter(email=email, code=code).exists():
            return Response(data='Неверный код', status=status.HTTP_400_BAD_REQUEST)
        return Response(data='Код подтвержден', status=status.HTTP_200_OK)
        
    
@extend_schema(tags=['Users Utils'])
@extend_schema_view(post=extend_schema(summary='СМЕНА ПАРОЛЯ ПОЛЬЗОВАТЕЛЯ'))
class UserClientForgotPasswordSetAPIView(APIView):
    serializer_class = serializers.EmailConfirmationSetSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        code = serializer.validated_data['code']
        password = serializer.validated_data['password']
        confirm_password = serializer.validated_data['confirm_password']
        if not models.ConfirmationCode.objects.filter(email=email, code=code).exists():
            return Response(data='Неверный код', status=status.HTTP_400_BAD_REQUEST)
        if password != confirm_password:
            return Response(data='Пароли не совпадают', status=status.HTTP_400_BAD_REQUEST)
        user = models.User.objects.get(email=email)
        user.set_password(password)
        user.save()
        return Response(data='Пароль успешно изменен', status=status.HTTP_200_OK)
    
    
    
    
@extend_schema(tags=['Auth'])
@extend_schema_view(post=extend_schema(summary='ВХОД В СИСТЕМУ'))
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
            'is_manager': user.is_manager,
        }, status=status.HTTP_200_OK)


@extend_schema(tags=['Auth'])
@extend_schema_view(post=extend_schema(summary='ОБНОВЛЕНИЕ ТОКЕНА'))
class UserRefreshAPIView(TokenRefreshView):
    serializer_class = serializers.UserRefreshSerializer


@extend_schema(tags=['Auth'])
@extend_schema_view(post=extend_schema(summary='ВЫХОД ИЗ СИСТЕМЫ'))
class UserLogoutAPIView(TokenBlacklistView):
    serializer_class = serializers.UserLogoutSerializer
