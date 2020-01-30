from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from pokemongogo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^callback$', views.callback)
]
