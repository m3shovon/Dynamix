from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.PersonalInfo)
admin.site.register(models.About)
admin.site.register(models.Education)
admin.site.register(models.Skill)
admin.site.register(models.WorkExperience)
admin.site.register(models.Interest)
admin.site.register(models.Certification)
