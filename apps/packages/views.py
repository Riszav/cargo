from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from config.permissions import *
from django.db.models import Q
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from . import models, serializers


@extend_schema(tags=['Посылки'])
@extend_schema(parameters=[
    OpenApiParameter('client', OpenApiTypes.STR, description='Клиент'),
    OpenApiParameter('recipient', OpenApiTypes.STR, description='Получатель'),
    OpenApiParameter('store', OpenApiTypes.STR, description='Склад'),
    OpenApiParameter('reys', OpenApiTypes.STR, description='Рейс'),
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
        if self.request.query_params.get('reys'):
            queryset = queryset.filter(reys=self.request.query_params.get('reys'))
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
        
        package = serializer.save()
        
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
                
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

@extend_schema(tags=['Посылки'])
class PackageDetailView(RetrieveUpdateAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    lookup_field = 'pk'
    permission_classes = [IsAdmin]
    
    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return serializers.PackageAdminCreateSerializer
        return serializers.PackageSerializer
    
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        package_details = serializer.validated_data.pop('package_details', [])
        package_images = serializer.validated_data.pop('package_images', [])
        package_weights = serializer.validated_data.pop('package_weights', [])
        
        package = serializer.save()
        
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
                
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        package_details = serializer.validated_data.pop('package_details', [])
        
        package = serializer.save(client=self.request.user)
        
        # Создаём связанные объекты, если их ещё нет
        if package_details:
            # Проверка на существование объекта
            for detail in package_details:
                models.PackageDetail.objects.get_or_create(package=package, **detail)
                
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['Посылки мои'])
class MyPackageDetailView(RetrieveUpdateAPIView):
    serializer_class = serializers.PackageCreateSerializer
    lookup_field = 'pk'
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(client=self.request.user)
        return queryset
    
    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        package_details = serializer.validated_data.pop('package_details', [])
        
        package = serializer.save()
        
        # Создаём связанные объекты, если их ещё нет
        if package_details:
            # Проверка на существование объекта
            for detail in package_details:
                models.PackageDetail.objects.update_or_create(package=package, **detail)
        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)


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


@extend_schema(tags=['Сканы'])
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
