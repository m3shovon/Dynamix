from django.db import models
# Create your models here.
# To create a custom user model and admin  model
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('User must have a email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """create and save a super user"""
        user = self.create_user(email, name, password)

        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    # Define the related_name for is_staff field
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='app_auth_users_is_staff'
    )

    # Define the related_name for is_active field
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='app_auth_users_is_active'
    )

    objects = UserProfileManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrive full name of the user"""
        return self.name

    def get_short_name(self):
        """Retrive short name of the user"""
        return self.name

    def __str__(self):
        """return string representation of our user"""
        return self.email

class Profile(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='profile' )
    username = models.CharField(max_length=100, blank=True)
    address1 = models.TextField(max_length=400, blank=True)
    city = models.CharField(max_length=40, blank=True)
    zipcode = models.CharField(max_length=10, blank=True)
    country = models.CharField(max_length=50, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    joined_date = models.DateField(auto_now_add=True)


    # alternate to views.py
    def __str__(self):
        return self.username + "'s Profile"

    # check all model is filled in the profile
    def is_fully_filled(self):
        fields_name = [f.name for f in self._meta.get_fields()]    

        for field_name in fields_name:
            value = getattr(self, field_name)
            if value is None or value == '':
                return False
        return True


# when user is create, profile will be create and they will be linked
# to automatically create Profile/one to one object

@receiver(post_save, sender=UserProfile)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=UserProfile)
def save_profile(sender, instance, **kwargs):
    instance.profile.save() #same as related name = profile













