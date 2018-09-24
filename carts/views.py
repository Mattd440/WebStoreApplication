from django.shortcuts import render

# Create your views here.

def cart_home(request):
    cart_id = request.session.get('cart_id', None)
    if cart_id is None :#and isinstance(cart_id, int):
        request.session['cart_id'] = 12
        print(request.session.get('cart_id'))
    else :
        print("cart exists")
        print(request.session.get('cart_id'))
    return render(request, 'carts/home.html')

