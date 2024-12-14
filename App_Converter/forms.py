from django import forms
from .models import ImageUpload, FileConversion

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


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
