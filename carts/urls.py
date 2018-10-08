from .views import *
from django.urls import re_path, path
from django.conf import settings

app_name='cart'

urlpatterns = [
    re_path(r'^$', cart_home, name='home'),
    re_path(r'^update/$', cart_update, name='update'),
    re_path(r'^checkout/$', checkout, name='checkout')
]
