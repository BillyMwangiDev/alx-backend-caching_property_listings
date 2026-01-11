"""
URL configuration for alx_backend_caching_property_listings project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('properties/', include('properties.urls')),
]
