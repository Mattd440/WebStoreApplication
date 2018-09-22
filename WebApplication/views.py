from django.shortcuts import render, redirect
from .forms import RegisterForm, ContactForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model

def home_page(request):
    return render(request, 'home_page.html')

def about_page(request):
    return render(request, 'home_page.html')

def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact_page.html', {'form':contact_form})

User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    #print("USR LOGGED IN" , request.user.authenticated())
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        email = form.cleaned_data.get('email')
        user = User.objects.create_user(username, email, password)
        print(user)
    return render(request, 'auth/login.html', {'form': form})

def login_page(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print(request.user.is_authenticated)
            # Redirect to a success page.
            redirect('/')
        else:
            # Return an 'invalid login' error message.
            print("error")

        print(form.cleaned_data)
    return render(request, 'auth/login.html', {'form':form})