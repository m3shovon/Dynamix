from django.urls import path
from . import views

app_name = 'App_Converter'

urlpatterns = [
    path('', views.home, name='home'),
    path('pdf-to-text/', views.pdf_to_text, name='pdf_to_text'),
    path('image-to-text/', views.image_to_text, name='image_to_text'),
    # path('remove-background/', views.remove_background, name='remove_background'),
    path('remove-background/', views.upload_image, name='upload_image'),
    path('convert-image/', views.convert_image, name='convert_image'),
    path('save-password/', views.save_password, name='save_password'),
    path('encrypt-password/', views.encrypt_password, name='encrypt_password'),
    path('decrypt-password/', views.decrypt_password, name='decrypt_password'),
    # path('doc-to-pdf/', views.doc_to_pdf, name='doc_to_pdf'),
    path('mp4-to-mp3/', views.mp4_to_mp3, name='mp4_to_mp3'),
    # path('download/<str:filename>/', views.download_text, name='download_text'),
]
