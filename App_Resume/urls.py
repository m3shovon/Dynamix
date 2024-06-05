from django.urls import path
from . import views

app_name = 'App_Resume'

urlpatterns = [
    path('', views.index, name='resume'),
]
