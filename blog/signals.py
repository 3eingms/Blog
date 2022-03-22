from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(user_logged_in,sender = User)
def login_success(sender,request,user,**kwargs):
    ip = request.META.get('REMOTE_ADDR')
    # print(ip)
    request.session['ip'] = ip