from django.contrib import admin
from .models import GuestEmail
from django.contrib.auth import get_user_model
# Register your models here.
admin.site.register(GuestEmail)

# User = get_user_model()
# admin.site.register(User)