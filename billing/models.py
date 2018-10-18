# from django.db import models
# from django.conf import settings
# from django.db.models.signals import post_save, pre_save
# from accounts.models import GuestEmail
#
# import stripe
# stripe.api_key= 'sk_test_R0KbGRdJEaj1yH0j0gZB62JH'
#
#
# # Create your models here.
# User = settings.AUTH_USER_MODEL
#
# # adds additional functionality to Billing Model
# class BillingProfileManager(models.Manager):
#     def new_or_get(self, request):
#         guest_email_id = request.session.get('guest_email_id')
#         created = False
#         user= request.user
#         billing_profile = None
#
#
#         # Logged In User CheckOut Remembers Payment Info
#         if user.is_authenticated:
#             billing_profile, created = self.model.objects.get_or_create(
#                 user=user, email=user.email)
#
#         # Guest Checkout auto reload payment info
#         elif guest_email_id is not None:
#             guest_email = GuestEmail.objects.get(id=guest_email_id)
#             billing_profile, created = self.model.objects.get_or_create(email=guest_email.email)
#
#         return billing_profile, created
#
# #Billing Model
# class BillingProfile(models.Model):
#     user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
#     email = models.EmailField()
#     active = models.BooleanField(default=True)
#     updated = models.DateTimeField(auto_now=True)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     customer_id = models.CharField(max_length=120, null=True, blank=True )
#
#     objects = BillingProfileManager()
#
#     def __str__(self):
#         return self.email
#
#
# def billing_profile_created_receiver(sender, instance, *args, **kwargs):
#     if not instance.customer_id and instance.email:
#         customer = stripe.Customer.create(
#             email = instance.email
#         )
#         instance.customer_id = customer.id
# pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)
#
#
# #Create a new billing profile whenever a user is created
# def user_created_receiver(sender,instance,created, *args, **kwargs):
#     if created and instance.email:
#         BillingProfile.objects.get_or_create(user=instance, email=instance.email)
#
# post_save.connect(user_created_receiver, sender=User)
#
# class CardManager(models.Manager):
#     def add_new(self, billing_profile, stripe_response):
#         if str(stripe_response.object) == 'card':
#             new_card = self.model(
#                 billing_profile = billing_profile,
#                 stripe_id = stripe_response.id,
#                 brand = stripe_response.brand,
#                 country = stripe_response.country ,
#                 exp_month = stripe_response.exp_month,
#                 exp_year = stripe_response.exp_year,
#                 last4 = stripe_response.last4
#             )
#             new_card.save()
#             return new_card
#         return None
#
#
# class Card(models.Model):
#     billing_profile=models.ForeignKey(BillingProfile, on_delete=models.DO_NOTHING)
#     stripe_id = models.CharField(max_length=120)
#     brand = models.CharField(max_length=120, null=True, blank=True)
#     country = models.CharField(max_length=120, null=True, blank=True)
#     exp_month = models.IntegerField(null=True, blank=True)
#     exp_year = models.IntegerField(null=True, blank=True)
#     last4 = models.CharField(max_length=120, null=True, blank=True)
#     #default = models.BooleanField(default=True)
#     objects = CardManager()
#
#     def __str__(self):
#         return "{} {}".format(self.brand, self.last4)

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from accounts.models import GuestEmail
User = get_user_model()

# abc@teamcfe.com -->> 1000000 billing profiles
# user abc@teamcfe.com -- 1 billing profile

import stripe
stripe.api_key = "sk_test_cu1lQmcg1OLffhLvYrSCp5XE"



class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if user.is_authenticated:
            'logged in user checkout; remember payment stuff'
            obj, created = self.model.objects.get_or_create(
                            user=user, email=user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reloads payment stuff'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                                            email=guest_email_obj.email)
        else:
            pass
        return obj, created

class BillingProfile(models.Model):
    user        = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)
    # customer_id in Stripe or Braintree

    objects = BillingProfileManager()

    def __str__(self):
        return self.email

def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    print(instance)
    if not instance.customer_id :
        print("ACTUAL API REQUEST Send to stripe/braintree")
        customer = stripe.Customer.create(
                email = instance.email
            )
        print(customer)
        instance.customer_id = customer.id

pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    print(instance)
    if created :
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)


class CardManager(models.Manager):
    def add_new(self, billing_profile, stripe_card_response):
        if str(stripe_card_response.object) == "card":
            new_card = self.model(
                    billing_profile=billing_profile,
                    stripe_id = stripe_card_response.id,
                    brand = stripe_card_response.brand,
                    country = stripe_card_response.country,
                    exp_month = stripe_card_response.exp_month,
                    exp_year = stripe_card_response.exp_year,
                    last4 = stripe_card_response.last4
                )
            new_card.save()
            return new_card
        return None


class Card(models.Model):
    billing_profile         = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    stripe_id               = models.CharField(max_length=120)
    brand                   = models.CharField(max_length=120, null=True, blank=True)
    country                 = models.CharField(max_length=20, null=True, blank=True)
    exp_month               = models.IntegerField(null=True, blank=True)
    exp_year                = models.IntegerField(null=True, blank=True)
    last4                   = models.CharField(max_length=4, null=True, blank=True)
    default                 = models.BooleanField(default=True)

    objects = CardManager()

    def __str__(self):
        return "{} {}".format(self.brand, self.last4)