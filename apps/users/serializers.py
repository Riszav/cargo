from rest_framework import serializers
from . import models


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
        fields = ['id', 'last_name', 'first_name', 'phone_number', 'email', 'password', 'country', 'address', 'passport_image_1', 'passport_image_2',]


class UserClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ['id', 'client_id', 'last_name', 'first_name', 'phone_number', 'email', 'password'
                  'tarif_usa', 'tarif_usa_value', 'tarif_turkey', 'tarif_turkey_value', 'tarif_china', 'tarif_china_value', 'tarif_japan', 'tarif_japan_value',]
