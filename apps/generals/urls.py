from django.urls import path
from . import views


urlpatterns = [
    path('banners/', views.BannerListView.as_view(), name='banner_list'),
    path('about-us/', views.AboutUsListView.as_view(), name='about_us_list'),
    path('about-us-page/', views.AboutUsPageListView.as_view(), name='about_us_page_list'),
    path('our-services/', views.OurServicesListView.as_view(), name='our_services_list'),
    path('application-settings/', views.ApplicationSettingsListView.as_view(), name='application_settings_list'),
    path('application/', views.ApplicationListView.as_view(), name='application_list'),
    path('faq/', views.FAQListView.as_view(), name='faq_list'),
    path('gallery/', views.GalleryListView.as_view(), name='gallery_list'),
    path('how-it-works/', views.HowItWorksListView.as_view(), name='how_it_works_list'),
    path('price-and-payment/', views.PriceAndPaymentListView.as_view(), name='price_and_payment_list'),
    path('payment-data/', views.PaymentDataListView.as_view(), name='payment_data_list'),
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('pvz/', views.PVZListView.as_view(), name='pvz_list'),
]