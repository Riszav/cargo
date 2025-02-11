from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('packages/<int:pk>/', views.PackageDetailView.as_view(), name='package_detail'),
    
    path('my-packages/', views.MyPackageListView.as_view(), name='my_package_list'),
    path('my-packages/<int:pk>/', views.MyPackageDetailView.as_view(), name='my_package_detail'),
    path('my-packages/status-count/', views.StatusCountView.as_view(), name='my_package_status_count'),
    
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('scans/', views.ScanListView.as_view(), name='scan_list'),
    path('scans/incoming/', views.ScanIncomingCreateView.as_view(), name='scan_incoming_create'),
    path('scans/outgoing/', views.ScanOutgoingCreateView.as_view(), name='scan_outgoing_create'),
    path('scans/location/', views.ScanLocationView.as_view(), name='scan_location'),
    
    path('awb/', views.AWBListView.as_view(), name='awb_list'),
]