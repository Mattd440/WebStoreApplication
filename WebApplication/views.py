from django.shortcuts import render, redirect
from .forms import ContactForm


def home_page(request):
    return render(request, 'home_page.html')

def about_page(request):
    return render(request, 'home_page.html')

def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        print(contact_form.cleaned_data)

    return render(request, 'contact_page.html', {'form':contact_form})

