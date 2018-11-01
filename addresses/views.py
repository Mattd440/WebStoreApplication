from django.shortcuts import render,redirect
from .forms import AddressForm
from billing.models import BillingProfile
from django.utils.http import is_safe_url
from .models import Address

# Controller for creating a new address
def checkout_address_create_view(request):
    # get form object
    form = AddressForm(request.POST or None)
    # get next url
    next = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next or next_post or None

    ## verify if form input is valid
    if form.is_valid():
        # get billing profile and address object
        billing_profile, created = BillingProfile.objects.new_or_get(request)
        instance = form.save(commit=False)

        # verify billing profile exists
        if billing_profile is not None:
            address_type = request.POST.get('address_type', 'shipping')
            instance.billing_profile = billing_profile
            instance.address_type = address_type
            instance.save()
            request.session[address_type + '_address_id'] = instance.id
            billing_address_id = request.session.get('billing_address_id', None)
            shipping_address_id = request.session.get('shipping_address_id', None)

        else:
            return redirect('cart:checkout')

        if is_safe_url(next_post, request.get_host()):
            return redirect(redirect_path)
        else:
            redirect('cart:checkout')
    return redirect('cart:checkout')

# controller for reusing an address
def checkout_address_reuse_view(request):
    if request.user.is_authenticated:
        next = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next or next_post or None

        # continue when request method is POST
        if request.method == 'POST':
            # get addresses and billing profile
            shipping_address = request.POST.get('shipping_address', None)
            address_type = request.POST.get('address_type', 'shipping')
            billing_profile, created = BillingProfile.objects.new_or_get(request)
           # verify address exists
            if shipping_address is not None:
                query = Address.objects.filter(billing_profile=billing_profile, id=shipping_address)
                if query.exists():
                    request.session[address_type + '_address_id'] =shipping_address

                if is_safe_url(next_post, request.get_host()):
                    return redirect(redirect_path)

    return redirect('cart:checkout')