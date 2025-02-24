from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.PackageListView.as_view(), name='package_list'),
    path('packages/<int:pk>/', views.PackageDetailView.as_view(), name='package_detail'),
    
    path('my-packages/', views.MyPackageListView.as_view(), name='my_package_list'),
    path('my-packages/<int:pk>/', views.MyPackageDetailView.as_view(), name='my_package_detail'),
    path('my-packages/status-count/', views.StatusCountView.as_view(), name='my_package_status_count'),
    path('my-packages/recipients/', views.MyRecipientListView.as_view(), name='my_recipient_list'),
    
    path('locations/', views.LocationListView.as_view(), name='location_list'),
    path('scans/', views.ScanListView.as_view(), name='scan_list'),
    path('scans/incoming/', views.ScanIncomingCreateView.as_view(), name='scan_incoming_create'),
    path('scans/outgoing/', views.ScanOutgoingCreateView.as_view(), name='scan_outgoing_create'),
    path('scans/location/', views.ScanLocationView.as_view(), name='scan_location'),
    
    path('awb/', views.AWBListView.as_view(), name='awb_list'),
    
    path('warehouse-data/', views.WarehouseDataView.as_view(), name='warehouse_data'),
    
    path('choices/products/', views.ProductsChoicesView.as_view(), name='choices_products'),
    path('choices/store/', views.StoreView.as_view(), name='choices_store'),
    path('choices/location/', views.LocationView.as_view(), name='choices_location'),
    path('choices/status/', views.PackageStatusView.as_view(), name='choices_status'),
    path('choices/recipient/', views.RecipientView.as_view(), name='choices_recipient'),
    path('choices/user/', views.UserView.as_view(), name='choices_user'),
]