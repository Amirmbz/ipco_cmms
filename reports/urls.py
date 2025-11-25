from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('workorder-status-summary/', views.workorder_status_summary, name='workorder_status_summary'),
    path('workorder-by-asset/', views.workorder_by_asset, name='workorder_by_asset'),
    path('workorder-by-technician/', views.workorder_by_technician, name='workorder_by_technician'),
    path('asset-history/', views.asset_history, name='asset_history'),
    path('pm-compliance/', views.pm_compliance, name='pm_compliance'),
    path('mtbf-mttr/', views.mtbf_mttr, name='mtbf_mttr'),
    path('inventory-consumption/', views.inventory_consumption, name='inventory_consumption'),
]