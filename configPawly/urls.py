"""
URL configuration for configPawly project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from SecurityApp import views as security_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', security_views.set_language, name='set_language'),  # cambiar el idioma
    path('', include('SecurityApp.urls')),
    path('', include('PawlyApp.urls')),
]


# Las fotos que suben los usuarios las sirve Django solo mientras se desarrolla
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
elif settings.SERVE_MEDIA:
    urlpatterns += [re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT})]
