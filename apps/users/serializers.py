from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['id', 'name', 'is_active']
        

class UserFullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'last_name', 'first_name']


class RecipientSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True)
    user = UserFullNameSerializer(read_only=True)
    class Meta:
        model = models.Recipient
        fields = ['id', 'last_name', 'first_name', 'phone_number', 'country', 'country_id', 'address', 'status_recipient',
                  'passport_number', 'passport_date', 'passport_place', 'passport_end_date', 'inn',  'date_of_birth', 
                  'passport_image_1', 'passport_image_2', 'portret_image', 'contract', 'user', 'main_recipient', 'created_at']  


class RecipientUserSerializer(RecipientSerializer):
    status_recipient = serializers.CharField(read_only=True)
    main_recipient = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = models.Recipient
        fields = ('id', 'last_name', 'first_name', 'status_recipient', 'address', 'country', 'country_id',
                  'phone_number', 'user', 'passport_image_1', 'passport_image_2', 'main_recipient', 'created_at')


class MyRecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipient
        fields = ['id', 'last_name', 'first_name']
        

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer(read_only=True)
    country_id = serializers.IntegerField(write_only=True)
    client_id = serializers.CharField(read_only=True)
    recipients = RecipientUserSerializer(many=True, required=False)
    class Meta:
        model = models.User
        fields = ['id', 'client_id', 'last_name', 'first_name', 'country', 'country_id', 'phone_number', 'email', 
                  'tarif_usa', 'tarif_usa_value', 'tarif_china', 'tarif_china_value',
                  'recipients']


class EmailConfirmationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)


class UserCreateSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=255)
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(min_length=8, max_length=50, write_only=True)
    country_id = serializers.IntegerField()
    address = serializers.CharField(max_length=255)
    passport_image_1 = serializers.ImageField()
    passport_image_2 = serializers.ImageField()
    # inn = serializers.CharField()
    # passport_number = serializers.CharField()
    # passport_date = serializers.DateField()
    # passport_place = serializers.CharField()


class UserClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    client_id = serializers.CharField(read_only=True)
    tarif_usa = serializers.CharField(read_only=True)
    tarif_usa_value = serializers.IntegerField(read_only=True)
    tarif_usa_weight = serializers.CharField(read_only=True)
    # tarif_turkey = serializers.CharField(read_only=True)
    # tarif_turkey_value = serializers.IntegerField(read_only=True)
    # tarif_turkey_weight = serializers.CharField(read_only=True)
    tarif_china = serializers.CharField(read_only=True)
    tarif_china_value = serializers.IntegerField(read_only=True)
    tarif_china_weight = serializers.CharField(read_only=True)
    # tarif_japan = serializers.CharField(read_only=True)
    # tarif_japan_value = serializers.IntegerField(read_only=True)
    # tarif_japan_weight = serializers.CharField(read_only=True)
    
    class Meta:
        model = models.User
        fields = ['id', 'client_id', 'last_name', 'first_name', 'phone_number', 'email',
                  'tarif_usa', 'tarif_usa_value', 'tarif_usa_weight', 'tarif_china', 'tarif_china_value', 'tarif_china_weight',]

class UserClientChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    confirm_password = serializers.CharField()


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserRefreshSerializer(TokenRefreshSerializer):
    pass


class UserLogoutSerializer(TokenBlacklistSerializer):
    pass
