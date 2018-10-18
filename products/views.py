from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Product
from django.http import Http404
from carts.models import Cart
from analytics.signals import object_viewed_signal
from analytics.mixins import ObjectViewMixin
# Create your views here.
#
#
# def product_list_view(request):
#     products= Product.objects.all()
#     context = {
#         'products' : products
#     }
#     return render(request, 'products/list.html', context)
#
#
# def product_detail_view(request, pk=None):
#
#     product = Product.objects.get_by_id(id=pk)
#     if product == None:
#         raise Http404('Product Not Found')
#     context = {
#         'product': product
#     }
#
#     return render(request, 'products/detail.html', context)
#
#
# def featured_view(request):
#     featured = Product.objects.features()
#     context = {
#         'products': featured
#     }
#     return render(request, 'products/list.html', context)
#
#
# def featured_detail_view(request, pk):
#     featured = Product.objects.features()
#     featured.get_by
#
#     if featured == None:
#         raise Http404('Product Not Found')
#     context = {
#         'product': featured
#     }
#
#     return render(request, 'products/detail.html', context)

class ProductDetailView(ObjectViewMixin,DetailView):
    model=Product
    queryset = Product.objects.all()
    template_name = 'products/detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        cart, new_cart = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context

    def get_object(self, *args, **kwargs):
        request = self.request
        slug = self.kwargs.get('slug')

        try:
            product = Product.objects.get(slug=slug, active=True)
        except Product.DoesNotExist:
            raise Http404("Product Not Found")
        except Product.MultipleObjectsReturned:
            query = Product.objects.filter(slug=slug, active=True)
            product= query.first()
        except:
            raise Http404("Cannot Find Product")

        #object_viewed_signal.send(product.__class__, instance=product, request=request)
        return product


class ProductListView( ListView):
    template_name = 'products/list.html'

    def get_queryset(self):
        request = self.request
        return Product.objects.all()

    def get_context_data(self, *args ,**kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        cart, new_cart = Cart.objects.new_or_get(self.request)
        context['cart'] = cart
        return context


#
# class ProductFeaturedListView(ObjectViewedMixin, ListView):
#     template_name = "products/list.html"
#
#     def get_queryset(self):
#         request = self.request
#         return Product.objects.all().featured()
#
# class ProductFeaturedDetailView(DetailView):
#     queryset = Product.objects.all().featured()
#     template_name = 'products/detail.html'