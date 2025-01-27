from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiTypes
from . import models, serializers


@extend_schema(tags=['Посылки'])
class PackageListView(ListAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    
    def get_queryset(self):
        queryset = self.queryset
        if self.request.query_params.get('status'):
            queryset = queryset.filter(status=self.request.query_params.get('status'))
        return queryset
    

@extend_schema(tags=['Посылки'])
class PackageDetailView(RetrieveUpdateAPIView):
    queryset = models.Package.objects.all()
    serializer_class = serializers.PackageSerializer
    lookup_field = 'pk'
    
    # def get_serializer_class(self):
    #     if self.request.method == 'GET':
    #         return serializers.PackageSerializer
    #     return serializers.PackageUpdateSerializer
    

@extend_schema(tags=['Посылки мои'])
class MyPackageOjidaemyeListView(ListAPIView):
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(user=self.request.user)
        queryset = queryset.filter(Q(status='Проверяется') | Q(status='Ждем на склад') | Q(status='На обработке') | 
                                   Q(status='Неправильный трекинг номер') | Q(status='Возвращена отправителю') | Q(status='Задержана на складе') | 
                                   Q(status='Отправлена') | Q(status='Прибыла') | Q(status='Доставлена заказчику') | Q(status='Отменена'))
        return queryset


@extend_schema(tags=['Посылки мои'])
class MyPackageNaSkladeListView(ListAPIView):
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(user=self.request.user, status='На складе')
        return queryset



@extend_schema(tags=['Посылки мои'])
class MyPackageOtpravlenoListView(ListAPIView):
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(user=self.request.user, status='Отправлена')
        return queryset
    


@extend_schema(tags=['Посылки мои'])
class MyPackagePribylaListView(ListAPIView):
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(user=self.request.user, status='Прибыла')
        return queryset
    

@extend_schema(tags=['Посылки мои'])
class MyPackagePoluchenaListView(ListAPIView):
    serializer_class = serializers.PackageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = models.Package.objects.filter(user=self.request.user, status='Доставлена заказчику')
        return queryset


@extend_schema(tags=['Сканы'])
@extend_schema(parameters=[
    OpenApiParameter('type', OpenApiTypes.STR, description='Тип сканы'),
    OpenApiParameter('country', OpenApiTypes.STR, description='Страна'),
    OpenApiParameter('tracking_number', OpenApiTypes.STR, description='Трек номер'),    
])
class ScanListView(ListAPIView):
    queryset = models.Scan.objects.all()
    serializer_class = serializers.ScanSerializer
    
    def get_queryset(self):
        queryset = self.queryset
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
class ScanIncomingCreateView(CreateAPIView):
    queryset = models.Scan.objects.all()
    serializer_class = serializers.ScanCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer['manager'] = request.user
        serializer['type'] = 'Входящие'
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(tags=['Сканы'])
class ScanOutgoingCreateView(CreateAPIView):
    queryset = models.Scan.objects.all()
    serializer_class = serializers.ScanCreateSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer['manager'] = request.user
        serializer['type'] = 'Исходящие'
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    

@extend_schema(tags=['Сканы'])
class ScanLocationView(CreateAPIView):
    queryset = models.Scan.objects.all()
    serializer_class = serializers.ScanCreateLocationSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer['manager'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
