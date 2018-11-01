from django.shortcuts import render
from products.models import  Product
from django.views.generic import ListView
from django.db.models import Q


# Controller for product search
class SearchProductView(ListView):

    # set parameters
    template_name = 'search/view.html'

    # set context
    def get_context_data(self, *args, **kwargs):
        context = super(SearchProductView, self).get_context_data(*args, **kwargs)
        context['query'] = self.request.GET.get('q')
        return context

    # query all products for searched for product

    def get_queryset(self, *args, **kwargs):
        request = self.request
        query = request.GET.get('q')

        if query is not None:
            return Product.objects.search(query)

        return  Product.objects.none()


