"""dns_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView, FormView
from userface import views

from django.urls import path, include # <--

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #path(r'^accounts/', include('allauth.urls')),
    url(r'^$', views.home, name='home'),
    url(r'^dashboard/$', views.index, name='dashboard'),
    url(r'^404.html', views.load404, name='404'),
    url(r'^run_query/$', views.run_backend_code, name='run_query'),
    url(r'^get_list_of_cached_files', views.get_list_of_cached_files, name='get_list_of_cached_files'),
    url(r'^dashboard/file_upload/$', views.simple_file_upload, name='file_upload'),
    url(r'^dashboard/file_download/$', views.simple_file_download, name='file_download')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
