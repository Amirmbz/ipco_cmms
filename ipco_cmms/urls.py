from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('api/accounts/', include('accounts.api')),
    path('api/plants/', include('plants.api')),
    path('api/locations/', include('locations.api')),
    path('api/assets/', include('assets.api')),
    path('api/inventory/', include('inventory.api')),
    path('api/work-orders/', include('work_orders.api')),
    path('api/maintenance/', include('maintenance.api')),
    path('api/reports/', include('reports.api')),
    path('api/notifications/', include('notifications.api')),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('plants/', include('plants.urls')),
    path('locations/', include('locations.urls')),
    path('assets/', include('assets.urls')),
    path('inventory/', include('inventory.urls')),
    path('work-orders/', include('work_orders.urls')),
    path('maintenance/', include('maintenance.urls')),
    path('reports/', include('reports.urls')),
    path('notifications/', include('notifications.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)