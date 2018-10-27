from django.contrib import admin
from .models import MailingPreference
# Register your models here.

class MailingPreferenceAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subscribed','updated']
    readonly_fields = [
        'mailchimp_subscribed',
        'timestamp',
        'updated'
    ]
    class Meta:
        model = MailingPreference
        fields = [
            'user',
            'subscribed',
            'mailchimp_msg',
            'mailchimp_subscribed',
            'timestamp',
            'updated'
        ]

admin.site.register(MailingPreference, MailingPreferenceAdmin)
