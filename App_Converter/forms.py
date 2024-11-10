from django import forms
from .models import ImageUpload

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImageUpload
        fields = ['image']


class DownloadForm(forms.Form):
    url = forms.URLField(
        label="Media URL", 
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Enter the media link'})
        )