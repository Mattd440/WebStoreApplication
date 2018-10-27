from django import forms

from .models import MailingPreference


class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive Marketing Email?', required=False)
    class Meta:
        model = MailingPreference
        fields = [
            'subscribed'
        ]