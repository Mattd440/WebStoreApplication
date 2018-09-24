"""WebApplication URL Configuration

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
from django.urls import path, re_path, include
from . import views
from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', views.home_page, name='home'),
    re_path('^about/$', views.about_page, name='about'),
    re_path('^contact/$', views.contact_page, name='contact'),
    re_path('^login/$', views.login_page, name='login'),
    re_path('^register/$', views.register_page, name='register'),
    re_path('^products/', include('products.urls', namespace='products')),
    re_path('^search/' , include('search.urls', namespace='search')),
    #re_path('^search/', include('search.urls', namespace='search'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


