from django.contrib import admin
from django.urls import path
from . import views
from . import views_auth
from .views_extern import ext_shop

urlpatterns = [
    path('index', views.indexpage, name='index' ),
    path('authenth', views_auth.reg_shop_user, name="authenth"),
    path('reg-shop', ext_shop.as_view(), name="reg"),
    path('lotery', views.lotery, name='lotery')
]