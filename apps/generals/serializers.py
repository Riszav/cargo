from rest_framework import serializers
from . import models


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Banner
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutUs
        fields = '__all__'


class AboutUsPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AboutUsPage
        fields = '__all__'
        

class OurServicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.OurServices
        fields = '__all__'


class ApplicationSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ApplicationSettings
        fields = '__all__'
        
        
class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Application
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FAQ
        fields = '__all__'
        

class GallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Gallery
        fields = '__all__'


class HowItWorksSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HowItWorks
        fields = '__all__'


class PriceAndPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PriceAndPayment
        fields = '__all__'


class PaymentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentData
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.News
        fields = '__all__'


class PVZSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PVZ
        fields = '__all__'

