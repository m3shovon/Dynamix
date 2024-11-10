from django.shortcuts import render,HttpResponseRedirect, redirect
from django.urls import reverse 
from django.http import HttpResponse
# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# form and model
from App_Auth.models import Profile, HitCounter
from App_Auth.forms import ProfileForm, SignUpForm
# Message
from django.contrib import messages #error, success, info, warning
from django.core.paginator import Paginator
from App_Auth.utils import send_mail_to_client
from lockdown.decorators import lockdown

#  Hit Count MiddlewareMixin
from django.utils.deprecation import MiddlewareMixin
from django.http import JsonResponse

# @lockdown()
@login_required
def dashboard(request):
    context = {
    }
    return render(request, 'App_Auth/dashboard.html', context)

def signup_user(request):
    form = SignUpForm()
    if request.method == "POST":
        form =  SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Account Created Successfully")
            return HttpResponseRedirect(reverse('App_Auth:signin'))
    return render(request, 'App_Auth/signup.html', context={'form':form})        


def signin_user(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username') #email is treated as username in model.py
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user) 
                return HttpResponseRedirect(reverse('App_Auth:dashboard'))
    return render(request, 'App_Auth/signin.html', context={'form': form})

# SIGNOUT
@login_required
def signout_user(request):
     logout(request)
     messages.warning(request, "You are Logged Out")
     return HttpResponseRedirect(reverse('App_Auth:signin'))

# Profile 
# @login_required
# def user_profile(request):
#     profile = Profile.objects.get(user=request.user)
#     form = ProfileForm(instance=profile)
#     if request.method == "POST":
#         form=ProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Profile Change Saved!")

#             form=ProfileForm(instance=profile)
#     return render(request, 'App_Auth/change_profile.html', context={'form': form})        


def send_mail(request):
    send_mail_to_client()
    print(send_mail_to_client)
    return redirect("/")

# 404 Error
def handle_not_found(request,exception):
	return render(request, "App_Auth/404.html")

#  Hit Count
# def increment_hit_count():
#     counter, created = HitCounter.objects.get_or_create(id=1)
#     counter.count += 1
#     counter.save()

def get_hit_count(request):
    counter = HitCounter.objects.first()
    hit_count = counter.count if counter else 0
    return JsonResponse({'hit_count': hit_count})