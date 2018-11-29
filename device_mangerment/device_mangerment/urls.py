"""device_mangerment URL Configuration

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
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from stark.service.stark import site

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^stark/', site.urls),
    # url(r'^login/$', views.login),
    url(r'^login/$', views.login_without),
    url(r'^users/$', views.users),
    url(r'^get_valid_img/$', views.get_valid_img),
    # url(r'^reg/$', views.register1),
    url(r'^reg/$', views.register),
    url(r'^index/$', views.index),
    url(r'^logout/$', views.log_out),
    url(r'^app01/', include('app01.urls')),
    url(r'^ajax_sw/$', views.ajax_sw),
    url(r'^ajax_sw_port/$', views.ajax_sw_port),
    url(r'^timer_ping/$', views.timer_ping),
]

