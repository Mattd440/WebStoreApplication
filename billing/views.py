

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.conf import settings
import stripe

# stripe api keys

STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_83u7mkT1hPNqTwh5gFewOBeg")
STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", 'sk_test_R0KbGRdJEaj1yH0j0gZB62JH')
stripe.api_key = STRIPE_SECRET_KEY

from .models import BillingProfile, Card

# controller for creating anew payment method
def payment_method_view(request):

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    print("bP {}".format(billing_profile))
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})



# ENd point for adding a new stripe card

def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        print("bP {}".format(billing_profile))
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status=401)
        token = request.POST.get("token")
        if token is not None:
            # customer = stripe.Customer.retrieve(billing_profile.customer_id)
            # card_response = customer.sources.create(source=token)
            new_card_obj = Card.objects.add_new(billing_profile, token)
            print(new_card_obj) # start saving our cards too!
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status=401)
