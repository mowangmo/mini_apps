from django.conf.urls import url
from django.contrib import admin
from app01 import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/', views.index),
    url(r'^add_book/', views.add_book),
    url(r'^edit/(\d+)', views.edit_book),
    url(r'^del/(\d+)', views.del_book),
    url(r'^query/', views.query),
]
