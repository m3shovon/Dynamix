from django.urls import path
from . import views

app_name = 'App_Converter'

urlpatterns = [
    path('', views.home, name='home'),
    path('pdf-to-text/', views.pdf_to_text, name='pdf_to_text'),
    path('image-to-text/', views.image_to_text, name='image_to_text'),
    path('remove-background/', views.upload_image, name='upload_image'),
    path('convert-image/', views.convert_image, name='convert_image'),
    path('download-video', views.download_yt, name='download_media'),
    path('generate-qr-code/', views.generate_qr_code, name='generate_qr_code'),
    path('save-password/', views.save_password, name='save_password'),
    path('encrypt-password/', views.encrypt_password, name='encrypt_password'),
    path('decrypt-password/', views.decrypt_password, name='decrypt_password'),
    path('hash-password/', views.hash_password, name='hash_password'),
    path('verify-password/', views.verify_password, name='verify_password'),
    path('mp4-to-mp3/', views.mp4_to_mp3, name='mp4_to_mp3'),
    path('ip/', views.get_url_info, name='get_url_info'),
    path('analyze-website/', views.analyze_website_view, name='analyze_website'),
    # path('doc-to-pdf/', views.doc_to_pdf, name='doc_to_pdf'),
    # path('download/<str:filename>/', views.download_text, name='download_text'),

]







