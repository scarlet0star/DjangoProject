"""MyCommunity URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path,include
from .views import *

from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler400,handler404,handler500

app_name = "main"

handler400 = 'MyCommunity.views.error400'
handler404 = 'MyCommunity.views.error404'
handler500 = 'MyCommunity.views.error500'

urlpatterns = [
    path('',homeView, name='home'),
    path('admin/', admin.site.urls),
    path('user/', include('userinfo.urls')),
    path('board/',include('board.urls')),
    path('summernote/',include('django_summernote.urls')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
