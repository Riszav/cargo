from rest_framework.generics import ListAPIView, CreateAPIView
from drf_spectacular.utils import extend_schema
from . import models, serializers


@extend_schema(tags=['ОБЩИЕ'])
class BannerListView(ListAPIView):
    queryset = models.Banner.objects.all()
    serializer_class = serializers.BannerSerializer


@extend_schema(tags=['ОБЩИЕ'])
class AboutUsListView(ListAPIView):
    queryset = models.AboutUs.objects.all()
    serializer_class = serializers.AboutUsSerializer
    

@extend_schema(tags=['ОБЩИЕ'])
class AboutUsPageListView(ListAPIView):
    queryset = models.AboutUsPage.objects.all()
    serializer_class = serializers.AboutUsPageSerializer
    

@extend_schema(tags=['ОБЩИЕ'])
class OurServicesListView(ListAPIView):
    queryset = models.OurServices.objects.all()
    serializer_class = serializers.OurServicesSerializer
    
    
@extend_schema(tags=['ОБЩИЕ'])
class ApplicationListView(CreateAPIView):
    queryset = models.Application.objects.all()
    serializer_class = serializers.ApplicationSerializer


@extend_schema(tags=['ОБЩИЕ'])
class FAQListView(ListAPIView):
    queryset = models.FAQ.objects.all()
    serializer_class = serializers.FAQSerializer
    

@extend_schema(tags=['ОБЩИЕ'])
class GalleryListView(ListAPIView):
    queryset = models.Gallery.objects.all()
    serializer_class = serializers.GallerySerializer
    

@extend_schema(tags=['ОБЩИЕ'])
class HowItWorksListView(ListAPIView):
    queryset = models.HowItWorks.objects.all()
    serializer_class = serializers.HowItWorksSerializer
    

@extend_schema(tags=['ОБЩИЕ'])
class PriceAndPaymentListView(ListAPIView):
    queryset = models.PriceAndPayment.objects.all()
    serializer_class = serializers.PriceAndPaymentSerializer
    

@extend_schema(tags=['ОБЩИЕ'])
class PaymentDataListView(ListAPIView):
    queryset = models.PaymentData.objects.all()
    serializer_class = serializers.PaymentDataSerializer
    
    
@extend_schema(tags=['ОБЩИЕ'])
class NewsListView(ListAPIView):
    queryset = models.News.objects.all()
    serializer_class = serializers.NewsSerializer


@extend_schema(tags=['ОБЩИЕ'])
class PVZListView(ListAPIView):
    queryset = models.PVZ.objects.all()
    serializer_class = serializers.PVZSerializer



