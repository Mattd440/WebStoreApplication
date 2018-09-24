from django.db import models
import random
import os
from django.db.models.signals import pre_save
from utils import unique_slug_generator
from django.urls import reverse
from django.db.models import Q


def upload_image_path(instance, filename):
    print(instance)
    print(filename)
    location = 'media/'
    basename = os.path.basename(filename)
    name, ext = os.path.splitext(basename)
    filename = name[:12] + str(random.randint(1,100000000))  +  ext
    return location + '/' + filename

class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        query_lookup = Q(title__icontains=query) \
                       | Q(description__icontains=query) \
                       |Q(price__icontains=query)

        return self.filter(query_lookup).distinct()



class ProductManager(models.Manager):
    def get_queryset(self):
        return  ProductQuerySet(self.model, using=self._db)

    def features(self):
        return self.get_queryset().featured()

    def all(self):
        return self.get_queryset().active()

    def get_by_id(self, id):
        query =  self.get_queryset().filter(id=id)

        if query.count() == 1:
            return query.first()

        return None

    def search(self, query):
        return self.get_queryset().search(query)

class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(default='abc', blank=True, unique=True)
    description = models.CharField(max_length=120)
    price = models.DecimalField(decimal_places=2 , max_digits=10, default=39.99)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)


    objects = ProductManager()

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug':self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Product)