from django.urls.conf import re_path

from app_cart.views import *


urlpatterns = [
    re_path(r'^$', cart_detail, name='cart_detail'),
    re_path(r'^add/(?P<product_id>\d+)/$', cart_add, name='cart_add'),
    re_path(r'^drop/(?P<product_id>\d+)/$', cart_reduce, name='cart_reduce'),
    re_path(r'^remove/(?P<product_id>\d+)/$', cart_remove, name='cart_remove'),
]
