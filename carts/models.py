from django.db import models
from django.conf import settings
from products.models import Product
from django.db.models.signals import m2m_changed, pre_save
# Create your models here.

User= settings.AUTH_USER_MODEL

class CartManager(models.Manager):
    def new_or_get(self,request):
        cart_id = request.session.get('cart_id', None)
        query = self.get_queryset().filter(id=cart_id)

        if query.count() == 1:
            new_cart = False
            cart_obj = query.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            new_cart = True
            cart_obj = Cart.objects.new(user=request.user)
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_cart

    def new(self, user=None):
        current_user = None
        if user is not None:
            if user.is_authenticated:
                current_user = user
        return self.model.objects.create(user=current_user)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)

def m2mfield_changed_cart_receiver(sender, instance,action, *args, **kwargs):

    if action == 'post_add' or action == 'post_remove' or action == 'post_clear' :
        products = instance.products.all()
        total = 0

        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()

m2m_changed.connect(m2mfield_changed_cart_receiver,sender=Cart.products.through)


def pre_save_cart_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = float(instance.subtotal) * float(1.08)
    else:
        instance.total = 0

pre_save.connect(pre_save_cart_receiver, sender=Cart)