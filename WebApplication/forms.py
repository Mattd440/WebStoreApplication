from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Full Name',
               'class': 'form-control', 'id':'form-fullname'}))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder':'Email Address'
        }
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={'class':'form-control',
               'placeholder': "Your Message"}
    ))

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if not 'gmail.com' in email:
    #         raise forms.ValidationError("Email must be gmail.com")
    #     return email





