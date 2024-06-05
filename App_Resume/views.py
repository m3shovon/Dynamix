from django.shortcuts import render,HttpResponseRedirect, redirect
from django.urls import reverse 
from django.http import HttpResponse
# Authentication
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
# form and model
from App_Auth.models import Profile
from App_Auth.forms import ProfileForm, SignUpForm
# Message
from django.contrib import messages #error, success, info, warning
from django.core.paginator import Paginator
from App_Auth.utils import send_mail_to_client
from lockdown.decorators import lockdown

# @lockdown()
@login_required
def index(request):
    context = {
    }
    return render(request, 'App_Resume/index.html', context)
