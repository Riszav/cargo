from rest_framework import serializers
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
        fields = ['id', 'last_name', 'first_name', 'status_recipient', 'inn', 'country', 'country_id', 'passport_number', 'passport_date', 'passport_place', 
                  'phone_number', 'user', 'passport_image_1', 'passport_image_2', 'created_at']  


class RecipientChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Recipient
        fields = ['id', 'last_name', 'first_name', 'status_recipient', 'inn', 'country', 'passport_number', 'passport_date', 'passport_place', 
                  'phone_number', 'user', 'passport_image_1', 'passport_image_2', 'created_at']  


class RecipientUserSerializer(RecipientSerializer):
    edit_recipient = serializers.BooleanField(read_only=True)
    class Meta(RecipientSerializer.Meta):
        ordering = ['main_recipient', '-created_at']
        
    def create(self, validated_data):
        user = self.context['request'].user
        country = models.Country.objects.get(id=validated_data['country_id'])
        recipient = models.Recipient.objects.create(user=user, country=country, **validated_data)
        return recipient
        

class UserSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    recipients = RecipientUserSerializer(many=True)
    class Meta:
        model = models.User
        fields = ['id', 'client_id', 'last_name', 'first_name', 'country', 'phone_number', 'email', 
                  'tarif_usa', 'tarif_usa_value', 'tarif_turkey', 'tarif_turkey_value', 'tarif_china', 'tarif_china_value', 'tarif_japan', 'tarif_japan_value',
                  'recipients']


class UserCreateSerializer(serializers.Serializer):
    last_name = serializers.CharField(max_length=255)
    first_name = serializers.CharField(max_length=255)
    phone_number = serializers.CharField(max_length=20)
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(max_length=255, write_only=True)
    country_id = serializers.IntegerField()
    address = serializers.CharField(max_length=255)
    passport_image_1 = serializers.ImageField(required=False)
    passport_image_2 = serializers.ImageField(required=False)
    inn = serializers.CharField()
    passport_number = serializers.CharField()
    passport_date = serializers.DateField()
    passport_place = serializers.CharField()


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
