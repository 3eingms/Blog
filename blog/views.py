

from django.core.cache import cache
from django.shortcuts import render,HttpResponseRedirect
from .forms import SignUp,LoginForm,PostForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from .models import Post
from django.contrib.auth.models import Group

# Create your views here.
#home
def home(request):
    posts = Post.objects.all()
    return render(request,'blog/index.html',{'post':posts})

# about
def about(request):
    return render(request,'blog/about.html')

# contact
def contact(request):
    return render(request,'blog/contact.html')

# dashboard
def dashboard(request):
    if request.user.is_authenticated:
        posts  = Post.objects.all()
        
        # display profile
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ip = request.session.get('ip',0)
        
        # login count
        ct = cache.get('count',version=user.pk) 
        
        return render(request,'blog/dashboard.html',{'posts':posts,'full_name':full_name,'group':gps,'ip':ip,'ct':ct})
    else:
        return HttpResponseRedirect('/login/')

# login 
def user_login(request):
    # if not request.user.is_authenticated:
        if request.method == 'POST':
            form = LoginForm(request = request,data = request.POST)
        else:
            form = LoginForm()    
        if form.is_valid():
            uname = form.cleaned_data['username']
            upass = form.cleaned_data['password']
            user = authenticate(username=uname,password = upass)    
            if user is not None:
                login(request,user)    
                # messages.success(request,'Logged in Successfully')
                return HttpResponseRedirect('/dashboard/')
 
        return render(request,'blog/login.html',{'login':form})
    # else:
    #     return HttpResponseRedirect('/dashboard/')
    
# signup 
def signup(request):
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            messages.success(request,'Account Created Successfully! Ready to Rock')
            user = form.save()
            group = Group.objects.get(name='Author') #for adding users in  'author' group
            user.groups.add(group)

    else:
        form = SignUp()        
    return render(request,'blog/signup.html',{'form':form})

# logout 
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
        
   
# add post
def addPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            addpost = PostForm(request.POST)
            if addpost.is_valid():
                btitle = addpost.cleaned_data['title']
                bdesc = addpost.cleaned_data['desc']
                postmode = Post(title = btitle,desc = bdesc)
                postmode.save()
                addpost = PostForm()   
        else:
            addpost = PostForm()    
        return render(request,'blog/addpost.html',{'addpost':addpost})
    else:
        return HttpResponseRedirect('/login/')
    
    
# update/Edit post
def updatePost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi  = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)        
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')    
    

# delete post
def deletePost(request,id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            pi = Post.objects.get(pk=id)
            pi.delete()
            return HttpResponseRedirect('/dashboard/')
        
    else:
        return HttpResponseRedirect('/login/')