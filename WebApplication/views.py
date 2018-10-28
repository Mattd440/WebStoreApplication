from django.shortcuts import render, redirect
from .forms import ContactForm
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from products.models import Product
def home_page(request):
    featured = Product.objects.features()
    print("fefaf")
    print(featured)
    return render(request, 'home_page.html',{'featured_prods':featured})

def service_page(request):
    return render(request, 'services.html')

def contact_page(request):
    contact_form = ContactForm(request.POST or None)

    if contact_form.is_valid():
        data = contact_form.cleaned_data
        name =data.get('fullname')
        email = data.get('email')
        content = data.get('content')
        print("content {}".format(content))
        email = EmailMessage('Rocket Technology', content,'mmdiederick@gmail.com')
        email.send()
        if request.is_ajax():
            return JsonResponse({"message":"Thank You For Your Submission", 'name':name,
                                 'email':email, 'content':content})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')
    return render(request, 'contact_page.html', {'form':contact_form, 'content':" Welcome to the contact page."})

