from django import forms
from .models import ImageUpload, FileConversion, QRCode
from django.core.validators import FileExtensionValidator
from django.conf import settings

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload  # Specify your model here
        fields = ['image']  # Only include the image field in the form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].validators = [
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png']),
        ]
        self.fields['image'].help_text = f"Maximum file size: {settings.FILE_UPLOAD_MAX_MEMORY_SIZE/(1024*1024)}MB"

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise forms.ValidationError(
                    f"File too large. Maximum size is {settings.FILE_UPLOAD_MAX_MEMORY_SIZE/(1024*1024)}MB."
                )
        return image


class DownloadForm(forms.Form):
    url = forms.URLField(
        label="Media URL", 
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter the media link'})
        )

class EncryptDecryptForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea, label='Text')
    algorithm = forms.ChoiceField(choices=[
        ('AES', 'AES'),
        ('DES', 'DES'),
    ])

class FileConversionForm(forms.ModelForm):
    class Meta:
        model = FileConversion
        fields = ['doc_file', 'video_file']

class QRCodeForm(forms.ModelForm):
    class Meta:
        model = QRCode
        fields = ['url']