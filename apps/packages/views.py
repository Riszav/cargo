from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from config.permissions import *
from django.db.models import Q, Count
from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from . import models, serializers
from apps.users import models as users_models
from apps.users import serializers as users_serializers
from config.choices import *


@extend_schema(tags=['Посылки'])
@extend_schema(parameters=[
    OpenApiParameter('client', OpenApiTypes.STR, description='Клиент'),
    OpenApiParameter('recipient', OpenApiTypes.STR, description='Получатель'),
    OpenApiParameter('store', OpenApiTypes.STR, description='Склад'),
    OpenApiParameter('reys_year', OpenApiTypes.STR, description='Рейс год'),
    OpenApiParameter('reys_number', OpenApiTypes.STR, description='Рейс номер'),
    OpenApiParameter('status', OpenApiTypes.STR, description='Статус'),
    OpenApiParameter('date_from', OpenApiTypes.STR, description='Дата от'),
    OpenApiParameter('date_to', OpenApiTypes.STR, description='Дата до'),
    OpenApiParameter('date_on_warehouse_from', OpenApiTypes.STR, description='Дата на складе от'),
    OpenApiParameter('date_on_warehouse_to', OpenApiTypes.STR, description='Дата на складе до'),
])
class PackageListView(ListCreateAPIView):
    permission_classes = [IsAdminOrManager]
    
    def get_queryset(self):
        queryset = models.Package.objects.all()
        if self.request.query_params.get('client'):
            queryset = queryset.filter(client=self.request.query_params.get('client'))
        if self.request.query_params.get('recipient'):
            queryset = queryset.filter(recipient=self.request.query_params.get('recipient'))
        if self.request.query_params.get('store'):
            queryset = queryset.filter(store=self.request.query_params.get('store'))
        if self.request.query_params.get('reys_year'):
            queryset = queryset.filter(reys__year=self.request.query_params.get('reys_year'))
        if self.request.query_params.get('reys_number'):
            queryset = queryset.filter(reys__number=self.request.query_params.get('reys_number'))
        if self.request.query_params.get('warehouse'):
            queryset = queryset.filter(warehouse=self.request.query_params.get('warehouse'))
        if self.request.query_params.get('status'):
            queryset = queryset.filter(status=self.request.query_params.get('status'))
        if self.request.query_params.get('date_from'):
            queryset = queryset.filter(date_from__gte=self.request.query_params.get('date_from'))
        if self.request.query_params.get('date_to'):
            queryset = queryset.filter(date_to__lte=self.request.query_params.get('date_to'))
        if self.request.query_params.get('date_on_warehouse_from'):
            queryset = queryset.filter(date_on_warehouse__gte=self.request.query_params.get('date_on_warehouse_from'))
        if self.request.query_params.get('date_on_warehouse_to'):
            queryset = queryset.filter(date_on_warehouse__lte=self.request.query_params.get('date_on_warehouse_to'))
        return queryset
        #         query &= (Q(client__last_name__icontains=term) | Q(client__first_name__icontains=term))
        #     queryset = queryset.filter(query)
        # recipient = self.request.query_params.get('recipient')
        # if recipient:
        #     recipient_terms = recipient.split() 
        #     query = Q()
        #     for term in recipient_terms:
        #         query &= (Q(recipient__last_name__icontains=term) | Q(recipient__first_name__icontains=term))
        #     queryset = queryset.filter(query)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.PackageAdminCreateSerializer
        return serializers.PackageSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        package_details = serializer.validated_data.pop('package_details', [])
        package_images = serializer.validated_data.pop('package_images', [])
        package_weights = serializer.validated_data.pop('package_weights', [])
        reys = serializer.validated_data.pop('reys', None)
        
        if reys:
            reys, _ = models.Reys.objects.get_or_create(year=reys['year'], number=reys['number'])
            
        package = serializer.save(reys=reys)
        
        # Создаём связанные объекты, если их ещё нет
        if package_details:
            # Проверка на существование объекта
            for detail in package_details:
                models.PackageDetail.objects.get_or_create(package=package, **detail)
        
        if package_images:
            for image in package_images:
                models.PackageImage.objects.get_or_create(package=package, **image)
        
        if package_weights:
            for weight in package_weights:
                models.PackageWeight.objects.get_or_create(package=package, **weight)
                
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Удаление деталей посылки'])
class PackageDetailsDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        models.PackageDetail.objects.filter(id=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@extend_schema(tags=['Удаление деталей посылки'])
class PackageImagesDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        models.PackageImage.objects.filter(id=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Удаление деталей посылки'])
class PackageWeightsDeleteView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, *args, **kwargs):
        models.PackageWeight.objects.filter(id=kwargs['pk']).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(tags=['Посылки'])
class PackageDetailView(RetrieveUpdateDestroyAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return serializers.PackageAdminCreateSerializer
        return serializers.PackageSerializer
    
    
    def perform_update(self, serializer):
        package_details = serializer.validated_data.pop('package_details', [])
        package_images = serializer.validated_data.pop('package_images', [])
        package_weights = serializer.validated_data.pop('package_weights', [])
        reys = serializer.validated_data.pop('reys', None)
        
        if reys:
            reys, _ = models.Reys.objects.get_or_create(year=reys['year'], number=reys['number'])
        
        package = serializer.instance
        
        # Создаём связанные объекты, если их ещё нет
        if package_details:
            # Проверка на существование объекта
            for detail in package_details:
                models.PackageDetail.objects.update_or_create(package=package, **detail)
        
        if package_images:
            for image in package_images:
                models.PackageImage.objects.update_or_create(package=package, **image)
        
        if package_weights:
            for weight in package_weights:
                models.PackageWeight.objects.update_or_create(package=package, **weight)
        
        return serializer.save(reys=reys)


@extend_schema(tags=['Посылки мои'])
@extend_schema(parameters=[
    OpenApiParameter('status', OpenApiTypes.STR, description='Статус'),
])
class MyPackageListView(ListCreateAPIView):
    serializer_class = serializers.PackageCreateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(client=self.request.user)
        if self.request.query_params.get('status'):
            queryset = queryset.filter(status=self.request.query_params.get('status')) 
        return queryset
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        package_details = serializer.validated_data.pop('package_details', [])
        
        package = serializer.save(client=self.request.user)
        
        # Создаём связанные объекты, если их ещё нет
        if package_details:
            # Проверка на существование объекта
            for detail in package_details:
                models.PackageDetail.objects.get_or_create(package=package, **detail)
                
        # headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(tags=['Посылки мои'])
class MyPackageDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.PackageCreateSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(client=self.request.user)
        return queryset
    
    def perform_update(self, serializer):
        package_details = serializer.validated_data.pop('package_details', [])
        
        package = serializer.instance
        
        # Создаём связанные объекты, если их ещё нет
        if package_details:
            # Проверка на существование объекта
            for detail in package_details:
                models.PackageDetail.objects.update_or_create(package=package, **detail)
        
        return serializer.save()

@extend_schema(tags=['Посылки мои'])
class StatusCountView(ListAPIView):
    serializer_class = serializers.PackageStatusCountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(client=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        status_count = {}
        for status in queryset.values('status').distinct():
            status_count[status['status']] = queryset.filter(status=status['status']).count()
        if status_count:
            return Response([status_count,])
        return Response([])
    

@extend_schema(tags=['Посылки мои'])
class MyRecipientListView(ListAPIView):
    serializer_class = users_serializers.MyRecipientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = users_models.Recipient.objects.filter(user=self.request.user, status_recipient='Подтвержден')
        return queryset

class LocationListView(ListAPIView):
    serializer_class = serializers.LocationSerializer
    queryset = models.Location.objects.all()
    permission_classes = [IsAdmin]


@extend_schema(tags=['Сканы'])
@extend_schema(parameters=[
    OpenApiParameter('type', OpenApiTypes.STR, description='Тип сканы'),
    OpenApiParameter('country', OpenApiTypes.STR, description='Страна'),
    OpenApiParameter('tracking_number', OpenApiTypes.STR, description='Трек номер'),    
])
class ScanListView(ListAPIView):
    serializer_class = serializers.ScanSerializer
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = models.Scan.objects.all()
        if self.request.query_params.get('type') == 'incoming':
            queryset = queryset.filter(type='Входящие')
        elif self.request.query_params.get('type') == 'outgoing':
            queryset = queryset.filter(type='Исходящие')
            
        if self.request.query_params.get('country'):
            queryset = queryset.filter(manager__country=self.request.query_params.get('country'))
        
        if self.request.query_params.get('tracking_number'):
            queryset = queryset.filter(tracking_number__icontains=self.request.query_params.get('tracking_number'))
            
        return queryset


@extend_schema(tags=['Сканы'])
class ScanIncomingCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = models.Scan.objects.filter(type='Входящие')
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ScanCreateSerializer
        return serializers.ScanSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(manager=request.user, type='Входящие')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['Сканы'])
class ScanOutgoingCreateView(ListCreateAPIView):
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = models.Scan.objects.filter(type='Исходящие')
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ScanCreateSerializer
        return serializers.ScanSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(manager=request.user, type='Исходящие')
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

@extend_schema(tags=['Сканы'])
class ScanLocationView(ListCreateAPIView):
    permission_classes = [IsAdmin]
    
    def get_queryset(self):
        queryset = models.Scan.objects.exclude(location=None)
        return queryset
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.ScanCreateLocationSerializer
        return serializers.ScanSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(manager=request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['AWB'])
class AWBListView(ListCreateAPIView):
    serializer_class = serializers.AWBSerializer
    queryset = models.AWB.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    

@extend_schema(tags=['AWB'])
class AWBDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.AWBSerializer
    queryset = models.AWB.objects.all()
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'pk'


@extend_schema(tags=['Склады'])
class WarehouseDataView(ListAPIView):
    queryset = models.WarehouseData.objects.all()
    serializer_class = serializers.WarehouseDataSerializer
    permission_classes = [IsAuthenticated]
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response([{
            'id': item['id'],
            'usa': {
                'usa_address_1': item['usa_address_1'],
                'usa_address_2': f'{item["usa_address_2"]}-{request.user.client_id}',
                'usa_city': item['usa_city'],
                'usa_state': item['usa_state'],
                'usa_zip_code': item['usa_zip_code'],
                'usa_phone': item['usa_phone'],
            },
            'china': {
                'china_address': f'{item["china_address"]}-{request.user.client_id}',
                'china_phone': item['china_phone'],
                'china_region': item['china_region'],
                'china_detail_address': item['china_detail_address'],
                'china_post_code': item['china_post_code'],
            },
        } for item in serializer.data])


@extend_schema(tags=['Choices'])
class ProductsChoicesView(ListAPIView):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategoryChoicesSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Choices'])
class StoreView(ListAPIView):
    queryset = models.Store.objects.all()
    serializer_class = serializers.StoreSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Choices'])
class LocationView(ListAPIView):
    queryset = models.Location.objects.all()
    serializer_class = serializers.LocationSerializer
    permission_classes = [IsAuthenticated]


@extend_schema(tags=['Choices'])
class PackageStatusView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(STATUS_CHOICES)


@extend_schema(tags=['Choices'])
class RecipientView(ListAPIView):
    queryset = users_models.Recipient.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = users_models.Recipient.objects.filter(status_recipient='Подтвержден')
        return queryset


@extend_schema(tags=['Choices'])
class UserView(ListAPIView):
    queryset = users_models.User.objects.all()
    serializer_class = serializers.ClientSerializer
    permission_classes = [IsAuthenticated]
    
            
@extend_schema(tags=['Choices'])
class ReysView(APIView):
    # permission_classes = [IsAdminOrManager]
    
    def get(self, request, *args, **kwargs):
        reys = models.Reys.objects.all().order_by('year', 'number').values('year', 'number').distinct()
        return Response(reys)

