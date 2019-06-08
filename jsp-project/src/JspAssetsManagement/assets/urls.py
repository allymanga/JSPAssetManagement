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
from asset import views
from asset.views import index, register, category, asset_detail_view, list_view_two
from asset.views import (
    AssetDeleteView
)
from JSP import settings
from django.contrib.staticfiles.urls import static
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = "asset"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='home'),
    # path('dashboard/', list_view, name='dashboard'),
    path('dashboard/', list_view_two, name='dashboard'),
    path(r'<int:id>/delete/', AssetDeleteView.as_view(), name="asset-delete"),
    path('register/', register, name='register'),
    path('category/', category, name='category'),
    path(r'asset/<int:id>/', asset_detail_view, name='asset'),
    path(r'accounts/', include('allauth.urls')),
    path(r'asset/accounts/', include('allauth.urls')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
