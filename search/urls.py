from .views import *
from django.urls import re_path, path
from django.conf import settings

app_name='search'

urlpatterns = [
    re_path(r'^$', SearchProductView.as_view(), name='query'),

]

