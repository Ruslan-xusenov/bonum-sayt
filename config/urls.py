"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from market import views as market_views

urlpatterns = [
    path('django-secret-admin/', admin.site.urls),  # Django built-in admin (yashirin)
    path('adminnn/', market_views.admin_dashboard, name='admin_dashboard_redirect'),  # Custom admin panel
    path('accounts/', include('allauth.urls')),
    path('', include('market.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
