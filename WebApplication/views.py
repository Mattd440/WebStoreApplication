from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http import HttpResponse, JsonResponse


def home_page(request):
    return render(request, 'home_page.html')

def about_page(request):
    return render(request, 'home_page.html')

def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        print(contact_form.cleaned_data)
        if request.is_ajax():
            return JsonResponse({"message":"Thank You For Your Submission"})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, 'contact_page.html', {'form':contact_form})

