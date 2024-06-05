from django.urls import path
from . import views

app_name = 'App_Auth'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('signup/', views.signup_user, name='signup'),
    path('signin/', views.signin_user, name='signin'),
    path('signout/', views.signout_user, name='signout'),
    # path('profile/', views.user_profile, name='profile'),
    path('send-mail/', views.send_mail, name='send_mail'),
]
