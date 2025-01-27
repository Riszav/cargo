from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('packages/<int:pk>/', views.PackageDetailView.as_view(), name='package_detail'),
    
    path('my-packages/ojidaemye/', views.MyPackageOjidaemyeListView.as_view(), name='my_package_ojidaemye_list'),
    path('my-packages/na-sklade/', views.MyPackageNaSkladeListView.as_view(), name='my_package_na_sklade_list'),
    path('my-packages/otpravleno/', views.MyPackageOtpravlenoListView.as_view(), name='my_package_otpravleno_list'),
    path('my-packages/pribyla/', views.MyPackagePribylaListView.as_view(), name='my_package_pribyla_list'),
    path('my-packages/poluchena/', views.MyPackagePoluchenaListView.as_view(), name='my_package_poluchena_list'),
    
    path('scans/', views.ScanListView.as_view(), name='scan_list'),
    path('scans/incoming/', views.ScanIncomingCreateView.as_view(), name='scan_incoming_create'),
    path('scans/outgoing/', views.ScanOutgoingCreateView.as_view(), name='scan_outgoing_create'),
    path('scans/location/', views.ScanLocationView.as_view(), name='scan_location'),
]