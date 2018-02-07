from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^ajax_handle1/', views.ajax_handle1),
    url(r'^ajax_handle2/', views.ajax_handle2),
    url(r'^login/', views.login),
    url(r'^ajax_login/', views.ajax_login),
    url(r'^home/', views.home),
]
