from django.conf.urls import url
from django.contrib import admin
from app01 import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/', views.login),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^cpass/', views.cpass),
    url(r'^reg/', views.reg),
]
