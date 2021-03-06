from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

# Defines Form Fields to sign in a guest user
class GuestForm(forms.Form):
    email    = forms.EmailField()

# Defines Form Fields to login a user
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# Defines Form Fields To register a new user
# Defines restrictions on input fields
class RegisterForm(forms.Form):
    username = forms.CharField()
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError("Username is taken")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("email is taken")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("Passwords must match.")
        return data