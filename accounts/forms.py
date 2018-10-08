from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class GuestForm(forms.Form):
    email = forms.EmailField()

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