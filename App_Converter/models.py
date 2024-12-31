from django.db import models

class ImageUpload(models.Model):
    image = models.ImageField(upload_to='pre-convert/')
    processed_image = models.ImageField(upload_to='post-convert/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class DownloadHistory(models.Model):
    platform = models.CharField(max_length=50)
    url = models.URLField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.platform} - {self.url}"

class FileConversion(models.Model):
    doc_file = models.FileField(upload_to='docs/')
    video_file = models.FileField(upload_to='videos/')
    
    def __str__(self):
        return self.doc_file.name if self.doc_file else self.video_file.name
    
class QRCode(models.Model):
    url = models.URLField(max_length=200)
    qr_code_image = models.ImageField(upload_to='qr_codes/', blank=True, null=True)

    def __str__(self):
        return self.url



