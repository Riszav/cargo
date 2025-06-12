from rest_framework import serializers
from . import models
from apps.users import models as user_models
from apps.users import serializers as users_serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class ProductChoicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name']
        

class CategoryChoicesSerializer(serializers.ModelSerializer):
    products = ProductChoicesSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Category
        fields = ['id', 'name', 'products']


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Store
        fields = '__all__'
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'
        

class WarehouseDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WarehouseData
        fields = '__all__'
        

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    
    class Meta:
        model = models.Product
        fields = '__all__'

class PackageDetailSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    
    class Meta:
        model = models.PackageDetail
        fields = ['id', 'product', 'price', 'count']
        
class PackageDetailCreateSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    
    class Meta:
        model = models.PackageDetail
        fields = ['id', 'product', 'price', 'count']
        
class PackageImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageImage
        fields = ['id', 'image']
        
        
class PackageWeightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PackageWeight
        fields = ['id', 'count_place', 'weight', 'is_volume_weight', 'length', 'width', 'height', 'volume_weight']


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'tarif_usa', 'tarif_usa_value', 'tarif_china', 'tarif_china_value',]


class RecipientSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Recipient
        fields = ['id', 'first_name', 'last_name', 'user']


class ReysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Reys
        fields = ['id', 'year', 'number']


class PackageSerializer(serializers.ModelSerializer):
    package_details = PackageDetailSerializer(many=True, required=False, read_only=True)
    package_images = PackageImageSerializer(many=True, required=False, read_only=True)
    package_weights = PackageWeightSerializer(many=True, required=False, read_only=True)
    reys = ReysSerializer(read_only=True)
    store = StoreSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    recipient = ClientSerializer(read_only=True)
    
    class Meta:
        model = models.Package
        fields = '__all__'
        

class PackageCreateSerializer(serializers.ModelSerializer):
    package_details = PackageDetailCreateSerializer(many=True, required=False)
    status = serializers.CharField(read_only=True)
    reys = ReysSerializer(read_only=True)
    package_image = serializers.ImageField(required=False, read_only=True)
    label_image = serializers.ImageField(required=False, read_only=True)
    invoice_image = serializers.ImageField(required=False, read_only=True)
    # recipient = users_serializers.MyRecipientSerializer(read_only=True)
    # recipient_id = serializers.S(write_only=True)
    
    class Meta:
        model = models.Package
        fields = ['id', 'status', 'reys', 'warehouse', 'tracking_number', 'store', 'type_of_packaging', 'recipient', 'package_details', 
                  'package_image', 'label_image', 'invoice_image', 'client_comment',]
        
    # def get_recipient(self, obj):
    #     request = self.context.get('request')
    #     if request and request.user.is_authenticated:
    #         recipient = user_models.Recipient.objects.filter(user=request.user, status_recipient='Подтвержден').first()
    #         return recipient.id if recipient else None
    #     return None


class PackageAdminCreateSerializer(serializers.ModelSerializer):
    package_details = PackageDetailCreateSerializer(many=True, required=False)
    package_images = PackageImageSerializer(many=True, required=False)
    package_weights = PackageWeightSerializer(many=True, required=False)
    reys = ReysSerializer(required=False)
    
    class Meta:
        model = models.Package
        fields = ['id', 'client', 'recipient', 'status', 'warehouse', 'package_image', 'label_image', 'invoice_image', 'type_of_packaging', 'options_of_packaging',
                  'store', 'reys', 'full_name', 'weight_of_package', 'tracking_number', 'count_scans', 'final_weight', 'delivery_cost',
                  'system_comment', 'client_comment', 'cladovshik_comment', 'manager_comment', 'package_details', 'package_images', 'package_weights']
        
        
class PackageStatusCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Package
        fields = ['status',]
        
        
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.Country
        fields = ['id', 'name']

class ManagerSerializer(serializers.ModelSerializer):
    country = CountrySerializer()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'country']
        

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Location
        fields = ['id', 'name']
        

class ScanSerializer(serializers.ModelSerializer):
    manager = ManagerSerializer()
    location = LocationSerializer()
    
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


class AWBFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AWBFile
        fields = ('id', 'file')
        

class AWBSerializer(serializers.ModelSerializer):
    awb_files = AWBFileSerializer(many=True, required=False)
    reys = ReysSerializer(required=False)
    
    class Meta:
        model = models.AWB
        fields = ('id', 'number', 'count_place', 'weight', 'reys', 'date', 'warehouse', 'sender', 'recipient', 'comment', 'image', 'awb_files')
        
    def create(self, validated_data):
        awb_files = validated_data.pop('awb_files', [])
        awb = models.AWB.objects.create(**validated_data)
        for file in awb_files:
            models.AWBFile.objects.create(awb=awb, **file)
        return awb
