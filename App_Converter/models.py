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