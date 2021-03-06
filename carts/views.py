from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from order.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail
from addresses.forms import AddressForm
from addresses.models import Address
from django.http import JsonResponse
from django.conf import settings

import stripe

# Stripe api keys

STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_83u7mkT1hPNqTwh5gFewOBeg")
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", 'sk_test_R0KbGRdJEaj1yH0j0gZB62JH')
stripe.api_key = STRIPE_SECRET_KEY
publish_key = STRIPE_PUB_KEY

# controller to return cart data

def cart_detail_api_view(request):
    cart, newcart = Cart.objects.new_or_get(request)

    productData = [{
        "id":product.id,
        "url":product.get_absolute_url(),
        'name':product.title,
        'price':product.price
        } for product in cart.products.all()]
    cart = {'products':productData, 'subtotal':cart.subtotal, 'total':cart.total}
    return JsonResponse(cart)

# controller for main cart page returns cart object

def cart_home(request):
    cart, newcart = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart': cart})

# controller to execute when a cart is updated

def cart_update(request):
    prod_id = request.POST.get('product')

    if prod_id is not None:
        try:
            prod = Product.objects.get(id=prod_id)
        except Product.DoesNotExist:
            print("Product Does Not Exists")
            return redirect('cart:home')

        cart, new_cart = Cart.objects.new_or_get(request)

        if prod in cart.products.all():
            cart.products.remove(prod)
            product_added = False
        else:
            cart.products.add(prod)
            product_added = True
        request.session['cart_items'] = cart.products.count()
        print("cartitems {}".format(request.session.get('cart_items')))
        if request.is_ajax():
            print('ajax requested')
            json = {
                'added': product_added,
                'removed' : not product_added,
                'count': cart.products.count()
            }
            return JsonResponse(json, status=200)

    return redirect('cart:home')

# controller to complete checkout process

def checkout(request):
    # get card object
    cart, new_cart = Cart.objects.new_or_get(request)
    order = None

    # redirect if cart not present or no products in cart

    if new_cart or cart.products.count() == 0:
        return redirect('cart:home')

    # get form object
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()

    # get address ids
    billing_address_id  = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    # get billing profile
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    address_query = None
    has_card = False

    # check if profile exists
    if billing_profile is not None:
        # check if user is signed in
        if request.user.is_authenticated:
            address_query = Address.objects.filter(billing_profile=billing_profile)

        # get order object
        order, order_created = Order.objects.new_or_get(billing_profile=billing_profile,  cart=cart)

        # set orders shipping and billing addresses and save order
        if shipping_address_id:
            order.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order.billing_address = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if shipping_address_id or billing_address_id:
            order.save()

        # check if user has a saved card
        has_card = billing_profile.has_card

        # do if method is post
        if request.method == 'POST' :
            is_done = order.checkout_done()
            if is_done:
                charged_card, msg = billing_profile.charge(order)
                if charged_card:
                    order.mark_paid()
                    request.session['cart_items'] = 0
                    del request.session['cart_id']
                    return redirect('cart:success')
                else:
                    print(msg)
                    return redirect("cart:checkout")

    context = {
        'order':order,
        'billing_profile': billing_profile,
        'form':login_form,
        'guest_form':guest_form,
        'address_form': address_form,
        'address_query': address_query,
        'has_card': has_card,
        'publish_key': publish_key
        #'billing_address_form': billing_address_form
    }

    return render(request, 'carts/checkout.html', context)


# controller for thank you page

def checkout_done(request):
    return render(request, 'carts/checkout_done.html')