from django.contrib import admin
from App_Converter import models

# Register your models here.

admin.site.register(models.ImageUpload)

admin.site.register(models.DownloadHistory)

admin.site.register(models.FileConversion)

admin.site.register(models.QRCode)
