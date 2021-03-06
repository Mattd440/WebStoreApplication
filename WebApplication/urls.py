
from django.contrib import admin
from django.urls import path, re_path, include
from . import views
from django.conf import settings
#from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from carts.views import cart_home, cart_detail_api_view
from accounts.views import login_page, register_page, guest_login_page
from django.contrib.auth.views import LogoutView
from addresses.views import checkout_address_create_view, checkout_address_reuse_view
from billing.views import payment_method_view, payment_method_createview
from mailing.views import MailingPreferenceUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('^$', views.home_page, name='home'),
    re_path('^services/$', views.service_page, name='services'),
    re_path('^contact/$', views.contact_page, name='contact'),
    re_path('^login/$', login_page, name='login'),
    re_path('^checkout/address/create/$', checkout_address_create_view, name='checkout_address_create'),
    re_path('^checkout/address/reuse/$', checkout_address_reuse_view, name='checkout_address_reuse'),
    re_path('^logout/$', LogoutView.as_view(), name='logout'),
    re_path('^register/guest/$', guest_login_page, name='guest_register'),
    re_path('^register/$', register_page, name='register'),
    re_path('^products/', include('products.urls', namespace='products')),
    re_path('^search/' , include('search.urls', namespace='search')),
    re_path('^api/cart/$', cart_detail_api_view, name='api-cart'),
    re_path('^cart/',include('carts.urls', namespace='cart')),
    re_path('^billing/payment-method/$', payment_method_view, name='billing-payment-method'),
    re_path('^billing/payment-method/create/$', payment_method_createview, name='billing-payment-method-endpoint'),
    re_path('^settings/email/$', MailingPreferenceUpdateView.as_view(), name='settings'),

]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


