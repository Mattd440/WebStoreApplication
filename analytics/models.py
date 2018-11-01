from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.conf  import settings
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session
from django.db.models.signals import pre_save, post_save
# Create your models here.
User = get_user_model()
from .signals import  object_viewed_signal
from accounts.signals import user_logged_in


# analytics.models.py

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

FORCE_SESSION_TO_ONE = getattr(settings, 'FORCE_SESSION_TO_ONE', False)
FORCE_INACTIVE_USER_ENDSESSION = getattr(settings, 'FORCE_INACTIVE_USER_ENDSESSION', False)


# define analytic model for when an product is viewed
class ObjectViewed(models.Model):
    user            = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    content_type    = models.ForeignKey(ContentType, on_delete=models.SET_NULL, null=True)
    object_id       = models.PositiveIntegerField()
    ip_address      = models.CharField(max_length=120, blank=True, null=True)
    content_object  = GenericForeignKey('content_type', 'object_id')
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self, ):
        return "%s viewed: %s" %(self.content_object, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object Viewed'
        verbose_name_plural = 'Objects Viewed'

# method to execute when an product is viewed
def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)
    ip_address = None
    try:
        ip_address = get_client_ip(request)
    except:
        pass

    new_view_instance = ObjectViewed.objects.create(
                user=request.user,
                content_type=c_type,
                object_id=instance.id,
                ip_address=ip_address
                )
# define signal for product view
object_viewed_signal.connect(object_viewed_receiver)

#  User session creation analytical model
class UserSession(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING)
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    active = models.BooleanField(default=True)
    ended = models.BooleanField(default=False)

    def end_session(self):
        session_key = self.session_key
        ended = self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active=False
            self.ended=True
            self.save()
        except:
            pass
        return self.ended

#  method to execute when a user logs in
def post_save_session_receiver(sender, instance, created, *args, **kwargs):
    if created:
        query = UserSession.objects.filter(user=instance.user, ended=False, active=False).exclude(id=instance.id)
        for i in query:
            i.end_session()
    if not instance.active and not instance.ended :
        instance.end_session()
if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver, sender=UserSession)

# method to execute when a user session object changes
def post_save_user_changed_receiver(sender, instance, created, *args, **kwargs):
    if not created:
        if instance.is_active == False:
            query = UserSession.objects.filter(user=instance.user, ended=False, active=False)
            for i in query:
                i.end_session()

if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver, sender=User)

# method to execute whena user logs in
def user_logged_in_receiver(sender, instance, request, *args, **kwargs):
    user = instance
    ip_address = None
    session_key = None
    try:
        ip_address = get_client_ip(request)
        session_key = request.session.session_key
    except:
        pass
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )


user_logged_in.connect(user_logged_in_receiver)

# get users ip address
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip