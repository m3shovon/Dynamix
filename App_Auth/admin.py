from django.contrib import admin

# Register your models here.
from App_Auth import models

admin.site.register(models.UserProfile)
admin.site.register(models.Profile)
admin.site.register(models.HitCounter)
