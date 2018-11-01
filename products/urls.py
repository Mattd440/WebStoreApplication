from .views import *
from django.urls import re_path, path
from django.conf import settings

app_name='products'

# unique product urls

urlpatterns = [
    re_path(r'^$', ProductListView.as_view(), name='list'),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailView.as_view(), name='detail'),
]

