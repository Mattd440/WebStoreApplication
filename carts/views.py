from django.shortcuts import render, redirect
from .models import Cart
from products.models import Product
from order.models import Order
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from accounts.models import GuestEmail


def cart_home(request):
    cart, newcart = Cart.objects.new_or_get(request)
    print(cart.products)
    return render(request, 'carts/home.html', {'cart': cart})

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
        else:
            cart.products.add(prod)
        request.session['cart_items'] = cart.products.count()
    return redirect('cart:home')

def checkout(request):
    cart, new_cart = Cart.objects.new_or_get(request)
    order = None
    if new_cart or cart.products.count() == 0:
        return redirect('cart:home')
    else:
        order, new_order = Order.objects.get_or_create(cart=cart)

    user  = request.user
    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')

    if user.is_authenticated:
        billing_profile, profile_created = BillingProfile.objects.get_or_create(
                                                user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, profile_created = BillingProfile.objects.get_or_create(email=guest_email.email)
    else:
        pass

    return render(request, 'carts/checkout.html', {'order':order, 'billing_profile': billing_profile, 'form':login_form, 'guest_form':guest_form})