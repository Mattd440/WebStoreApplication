from django.db import models
from carts.models import Cart
from billing.models import BillingProfile
import math
# Create your models here.
from WebApplication.utils import unique_order_id_generator
from django.db.models.signals import pre_save, post_save
ORDER_STATUS = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, null=True, blank=True)
    order_id = models.CharField(default='abc', blank=True, max_length=120)
    cart =models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created')
    total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    shipping_total = models.DecimalField(default=5.99, max_digits=100, decimal_places=2)
    active = models.BooleanField(default=True)

    #billing_profile
    #shipping_address
    #billing_address

    def __str__(self):
        return self.order_id

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = math.fsum([cart_total,shipping_total])
        format_total = format(new_total, '.2f')
        self.total = format_total
        self.save()
        return new_total

def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance,created, *args, **kwargs):
    if not created:
        cart = instance
        total = cart.total
        cart_id = cart.id
        query = Order.objects.filter(cart__id=cart_id)

        if query.count() == 1:
            order = query.first()
            order.update_total()

post_save.connect(post_save_cart_total, sender=Cart)

def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()

post_save.connect(post_save_order, sender=Order)