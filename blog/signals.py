from ensurepip import version
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.cache import cache


@receiver(user_logged_in,sender = User)
def login_success(sender,request,user,**kwargs):
    # ge ip address
    ip = request.META.get('REMOTE_ADDR')
    # print(ip)
    request.session['ip'] = ip
    
    # for login count
    ct = cache.get('count',0,version = user.pk)
    newcount = ct + 1
    cache.set('count',newcount,version = user.pk)