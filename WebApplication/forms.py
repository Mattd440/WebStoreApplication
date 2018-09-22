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

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not 'gmail.com' in email:
            raise forms.ValidationError("Email must be gmail.com")
        return email

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirm Password" , widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username = username)
        if qs.exists():
            raise forms.ValidationError("Username is Taken")
        return username

    def clean_email(self):
        username = self.cleaned_data.get('email')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("An account with this email exists")
    def clean(self):
        data= self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 =self.cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("Passwords Must Match")

        return data


