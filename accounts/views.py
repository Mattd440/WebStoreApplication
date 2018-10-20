from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import RegisterForm, LoginForm, GuestForm
from .models import  GuestEmail
from django.utils.http import is_safe_url
from .signals import user_logged_in
# Create your views here.
User = get_user_model()
from django.urls import reverse

def guest_login_page(request):
    form = GuestForm(request.POST or None)

    next = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next or next_post or None

    if form.is_valid():
        guestemail= form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=guestemail)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(next_post, request.get_host()):
            return redirect(redirect_path)
        else:
            redirect('/register/')

    return redirect('/cart/checkout' ,{'form':None})

def register_page(request):
    form = RegisterForm(request.POST or None)

    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        print(user)

    return render(request, 'accounts/register.html', {'form': form})


def login_page(request):
    form = LoginForm(request.POST or None)

    next = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next or next_post or None

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, request=request, instance=user)
            try:
                del request.session['guest_email_id']
            except:
                pass

            if is_safe_url(next_post, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('home')
        else:
            # Return an 'invalid login' error message.
            print("error cannot login")

        print(form.cleaned_data)
    return render(request, 'accounts/login.html', {'form':form})