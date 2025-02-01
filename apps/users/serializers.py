from rest_framework import serializers
from . import models
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, TokenBlacklistSerializer

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Country
        fields = ['id', 'name', 'is_active']


class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    class Meta:
        model = models.User
        fields = ['id', 'client_id', 'last_name', 'first_name', 'country', 'phone_number', 'email', 
                  'tarif_usa', 'tarif_usa_value', 'tarif_turkey', 'tarif_turkey_value', 'tarif_china', 'tarif_china_value', 'tarif_japan', 'tarif_japan_value', 
                  'inn', 'status', 'passport_number', 'passport_date', 'passport_place', 'passport_image_1', 'passport_image_2', 'contract']


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'last_name', 'first_name', 'phone_number', 'email', 'password', 'country', 'address', 'passport_image_1', 'passport_image_2', 
                  'inn', 'passport_number', 'passport_date', 'passport_place']


class UserClientSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)
    phone_number = serializers.CharField(read_only=True)
    client_id = serializers.CharField(read_only=True)
    tarif_usa = serializers.CharField(read_only=True)
    tarif_usa_value = serializers.IntegerField(read_only=True)
    tarif_usa_weight = serializers.CharField(read_only=True)
    tarif_turkey = serializers.CharField(read_only=True)
    tarif_turkey_value = serializers.IntegerField(read_only=True)
    tarif_turkey_weight = serializers.CharField(read_only=True)
    tarif_china = serializers.CharField(read_only=True)
    tarif_china_value = serializers.IntegerField(read_only=True)
    tarif_china_weight = serializers.CharField(read_only=True)
    tarif_japan = serializers.CharField(read_only=True)
    tarif_japan_value = serializers.IntegerField(read_only=True)
    tarif_japan_weight = serializers.CharField(read_only=True)
    
    class Meta:
        model = models.User
        fields = ['id', 'client_id', 'last_name', 'first_name', 'phone_number', 'email',
                  'tarif_usa', 'tarif_usa_value', 'tarif_usa_weight', 'tarif_turkey', 'tarif_turkey_value', 'tarif_turkey_weight', 
                  'tarif_china', 'tarif_china_value', 'tarif_china_weight', 'tarif_japan', 'tarif_japan_value', 'tarif_japan_weight',]

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
