from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.contrib.auth import get_user_model
from .utils import Mailchimp


# define email marketing model
class MailingPreference(models.Model):
    user                        = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    subscribed                  = models.BooleanField(default=True)
    mailchimp_subscribed        = models.NullBooleanField(blank=True)
    mailchimp_msg               = models.TextField(null=True, blank=True)
    timestamp                   = models.DateTimeField(auto_now_add=True)
    updated                      = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email



##### method to execute when a mailing object is created #########


def mailing_pref_create_receiver(sender, instance, created, *args, **kwargs):
    if created:
        status_code, response_data = Mailchimp().subscribe(instance.user.email)
        print(status_code, response_data)


post_save.connect(mailing_pref_create_receiver, sender=MailingPreference)


# method to execute when mailing settings are changed

def mailing_pref_update_receiver(sender, instance, *args, **kwargs):
    if instance.subscribed != instance.mailchimp_subscribed:
        if instance.subscribed:
            # subscribing user
            print("subscrived")
            status_code, response_data = Mailchimp().subscribe(instance.user.email)
            print(status_code, response_data)
        else:
            # unsubscribing use
            print('unsubscribed')
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)


        if response_data['status'] == 'subscribed':
            instance.subscribed = True
            instance.mailchimp_subscribed = True
            instance.mailchimp_msg = response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

pre_save.connect(mailing_pref_update_receiver, sender=MailingPreference)



def make_mailing_pref_receiver(sender, instance, created, *args, **kwargs):

    if created:
        MailingPreference.objects.get_or_create(user=instance)

post_save.connect(make_mailing_pref_receiver, sender=get_user_model())