from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.utils.http import is_safe_url
from .models import BillingProfile, Card
# Create your views here.
import stripe
stripe.api_key= 'sk_test_R0KbGRdJEaj1yH0j0gZB62JH'
STRIPE_PUB_KEY = 'pk_test_83u7mkT1hPNqTwh5gFewOBeg'

# def payment_method_view(request):
#     billing_profile, created_profile = BillingProfile.objects.new_or_get(request)
#     if not billing_profile:
#         return redirect('/cart')
#
#     next_url = None
#     next = request.GET.get('next')
#
#     if is_safe_url(next, request.get_host()):
#         next_url = next
#     return render(request, 'billing/payment-method.html',
#                   {'publish_key': STRIPE_PUB_KEY, 'next_url': next_url} )
#
# def payment_method_createview(request):
#     if request.method == 'POST' and request.is_ajax():
#         billing_profile, created_profile = BillingProfile.objects.new_or_get(request)
#         if not billing_profile:
#             return HttpResponse({'message': 'Cannot Find User'}, status=401)
#
#         token = request.POST.get('token')
#         print(token)
#         if token is not None:
#             print(billing_profile)
#             customer = stripe.Customer.retrieve(billing_profile.customer_id)
#             card_response = customer.sources.create(source=token)
#             customer.save()
#             print(card_response)
#         return JsonResponse({'message': 'Success! Your card was added.'})
#     return HttpResponse('error', status=401)

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url




import stripe
stripe.api_key = "sk_test_cu1lQmcg1OLffhLvYrSCp5XE"
STRIPE_PUB_KEY = 'pk_test_PrV61avxnHaWIYZEeiYTTVMZ'

from .models import BillingProfile, Card

def payment_method_view(request):
    #next_url =
    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    print("bP {}".format(billing_profile))
    if not billing_profile:
        return redirect("/cart")
    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_
    return render(request, 'billing/payment-method.html', {"publish_key": STRIPE_PUB_KEY, "next_url": next_url})




def payment_method_createview(request):
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        print("bP {}".format(billing_profile))
        if not billing_profile:
            return HttpResponse({"message": "Cannot find this user"}, status=401)
        token = request.POST.get("token")
        if token is not None:
            customer = stripe.Customer.retrieve(billing_profile.customer_id)
            card_response = customer.sources.create(source=token)
            new_card_obj = Card.objects.add_new(billing_profile, card_response)
            print(new_card_obj) # start saving our cards too!
        return JsonResponse({"message": "Success! Your card was added."})
    return HttpResponse("error", status=401)
