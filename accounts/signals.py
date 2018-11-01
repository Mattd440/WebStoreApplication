from django.dispatch import Signal

# defines signal to trigger an action when a user signs in
user_logged_in = Signal(providing_args=[ 'instance','request'])