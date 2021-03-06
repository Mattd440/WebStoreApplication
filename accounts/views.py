from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from .forms import RegisterForm, LoginForm, GuestForm
from .models import  GuestEmail
from django.utils.http import is_safe_url
from .signals import user_logged_in
# Create your views here.
User = get_user_model()
from django.urls import reverse

from django.contrib.auth import authenticate, login, get_user_model
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url


from .forms import LoginForm, RegisterForm, GuestForm
from .models import GuestEmail

# controller for guest login

def guest_login_page(request):
    # get form object from request object
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    # get next url from request object
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    # verify if form input is valid
    if form.is_valid():
        email       = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("/register/")
    return redirect("/register/")

# controller for user log in page

def login_page(request):
    #get form object from request object

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    # get next url from request object

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    # verify if form input is valid
    if form.is_valid():
        username  = form.cleaned_data.get("username")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            # Return an 'invalid login' error message.
            print("Error")
    return render(request, "accounts/login.html", context)

# controller for registering a new user

def register_page(request):
    # get form object form request object

    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    # verify form is valid
    if form.is_valid():
        print(form.cleaned_data)
        username  = form.cleaned_data.get("username")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        # create new user
        new_user  = User.objects.create_user(username, email, password)
        #print(new_user)

    return render(request, "accounts/register.html", context)

#
