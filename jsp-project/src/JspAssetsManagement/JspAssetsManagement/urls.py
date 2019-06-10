"""JSP URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from assets import views
from assets.views import index, register, category, asset_detail_view, list_view_two, list_view_laptops, list_view_cars, list_view_printers, list_view_trucks, list_view_furniture, list_view_others, assets_worth, thank_you, renting_module, movement_module
from assets.views import index, list_view_two
from assets.views import (
    AssetDeleteView, AssetUpdateView
)
from . import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    path('thank-you/', thank_you, name='thank-you'),
    # path('dashboard/', list_view, name='dashboard'),
    path('dashboard/', list_view_two, name='dashboard'),
    path('category/laptops/', list_view_laptops, name='laptops'),
    path('category/cars/', list_view_cars, name='cars'),
    path('category/printers/', list_view_printers, name='printers'),
    path('category/trucks/', list_view_trucks, name='trucks'),
    path('category/furniture/', list_view_furniture, name='furniture'),
    path('category/others/', list_view_others, name='others'),
    # path('asset-id/', increment_booking_number, name='asset-id'),
    path('assets-rented/', renting_module, name='rented-assets'),
    path('assets-in-motion/', movement_module, name='assets-in-motion'),
    path('assets-worth/', assets_worth, name='assets-cost'),
    # path(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.list_view_two, name='show_category'),
    path(r'<int:id>/delete/', AssetDeleteView.as_view(), name="asset-delete"),
    path(r'<int:id>/update/', AssetUpdateView.as_view(), name="asset-update"),
    path('register/', register, name='register'),
    path('category/', category, name='category'),
    path(r'asset/<int:id>/', asset_detail_view, name='asset'),
    path(r'accounts/', include('allauth.urls')),
    path(r'assets/accounts/', include('allauth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)