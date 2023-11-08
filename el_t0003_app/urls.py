from django.urls import path
from . import views
from . import views_reg
from .views_ex_reg import ext_shop

urlpatterns = [
    path('gym', views.gympage, name='gym' ),
    path('reg', views_reg.reg_shop_user, name='reg'),
    path('reg-ext-shop', ext_shop.as_view(), name='shopreg'),
    path('ticket', views.ticketview, name='ticket')
]