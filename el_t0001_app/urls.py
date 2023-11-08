from django.contrib import admin
from django.urls import path
from . import views
from . import views_authenth
from .views_ext_reg import ext_shop_reg
from .views_shopgame import cab_cartpage

urlpatterns = [
    path('main/', views.mainpage, name = 'main'),
    path('choise/', views.choisepage, name = 'choise'),
    path('auth/<int:img_id>', views_authenth.register_shop_user, name = 'auth'),
    path('register-shopuser/<int:img_id>', ext_shop_reg.as_view(), name='ext_registr' ),
    path('game/<int:img_id>', cab_cartpage, name = 'game')
]