"""
Guardelio Root URL Configuration
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.progress.urls import simulation_urlpatterns, progress_urlpatterns

urlpatterns = [
    # Django built-in admin (for quick data inspection in dev)
    path('django-admin/', admin.site.urls),

    # API v1 — all application endpoints
    path('api/v1/auth/',        include('apps.accounts.urls')),
    path('api/v1/',             include('apps.scenarios.urls')),

    # Simulation and Progress are served at SEPARATE prefixes
    path('api/v1/simulation/',  include((simulation_urlpatterns, 'simulation'))),
    path('api/v1/progress/',    include((progress_urlpatterns,   'progress'))),

    # Admin portal
    path('api/v1/admin/',       include('apps.reports.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

