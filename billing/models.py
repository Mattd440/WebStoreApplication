from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from accounts.models import GuestEmail
# Create your models here.
User = settings.AUTH_USER_MODEL

# adds additional functionality to Billing Model
class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        guest_email_id = request.session.get('guest_email_id')
        created = False
        user= request.user
        billing_profile = None

        # Logged In User CheckOut Remembers Payment Info
        if user.is_authenticated:
            billing_profile, created = self.model.objects.get_or_create(
                user=user, email=user.email)

        # Guest Checkout auto reload payment info
        if guest_email_id is not None:
            guest_email = GuestEmail.objects.get(id=guest_email_id)
            billing_profile, created = self.model.objects.get_or_create(email=guest_email.email)

        return billing_profile, created

#Billing Model
class BillingProfile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = BillingProfileManager()
    def __str__(self):
        return self.email

#Create a new billing profile whenever a user is created
def user_created_receiver(sender,instance,created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)

post_save.connect(user_created_receiver, sender=User)