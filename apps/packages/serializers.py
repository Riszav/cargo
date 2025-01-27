from rest_framework import serializers
from . import models
from django.contrib.auth import get_user_model

User = get_user_model()


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    
    class Meta:
        model = models.Product
        fields = '__all__'

class PackageDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = models.PackageDetail
        fields = '__all__'
        
        
class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageImage
        fields = '__all__'
        
        
class PackageWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageWeight
        fields = '__all__'


class PackageSerializer(serializers.ModelSerializer):
    package_details = PackageDetailSerializer(many=True)
    package_images = PackageImageSerializer(many=True)
    package_weights = PackageWeightSerializer(many=True)
    store = StoreSerializer()
    
    class Meta:
        model = models.Package
        fields = '__all__'
        

class ManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'country']
        

class ScanSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    
    class Meta:
        model = models.Scan
        fields = ['id', 'tracking_number', 'tracking_number_2', 'manager', 'type', 'location', 'updated_at', 'created_at']


class ScanCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scan
        fields = ['tracking_number', 'tracking_number_2']
        
        
class ScanCreateLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Scan
        fields = ['tracking_number', 'tracking_number_2', 'location']
