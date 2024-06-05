from django.forms import ModelForm
from App_Auth.models import UserProfile, Profile
from django.contrib.auth.forms import UserCreationForm

# form 
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        exclude = ('user',)

class SignUpForm(UserCreationForm):
    class Meta:
        model  = UserProfile
        fields = ('email', 'name', 'password1', 'password2')
