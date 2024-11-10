from django.shortcuts import render
from django.http import JsonResponse
# import json
import requests

import fitz  
from django.http import HttpResponse
import os

from PIL import Image
import io

# Remove BG
from django.shortcuts import render, redirect
from .forms import ImageUploadForm, DownloadForm
from .models import ImageUpload, DownloadHistory
from rembg import remove
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from cryptography.fernet import Fernet
from docx import Document
# from weasyprint import HTML
from pydub import AudioSegment
from yt_dlp import YoutubeDL



def home(request):
    return render(request, 'App_Converter/home.html')

from django.http import HttpResponse
from django.urls import reverse

# def download_text(request, filename):
#     file_path = f'media/{filename}'
#     with open(file_path, 'rb') as f:
#         response = HttpResponse(f, content_type='text/plain')
#         response['Content-Disposition'] = f'attachment; filename="{filename}"'
#         return response

# PDF TO Text
def pdf_to_text(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf']
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        # Save text to a .txt file with UTF-8 encoding
        text_filename = "converted_pdf_to_text.txt"
        text_path = os.path.join('media', text_filename)
        
        # Write with UTF-8 encoding to avoid UnicodeEncodeError
        with open(text_path, 'w', encoding='utf-8') as f:
            f.write(text)

        # Provide file for download
        with open(text_path, 'r', encoding='utf-8') as f:
            response = HttpResponse(f, content_type='text/plain')
            response['Content-Disposition'] = f'attachment; filename={text_filename}'
            return response
    return render(request, 'App_Converter/pdf_to_text.html')


# Image To Text
def image_to_text(request):
    if request.method == 'POST':
        image_file = request.FILES['image']

        # Prepare the request to OCR.space API
        api_key = 'K81007853788957'  # testnetworkeverything@gmail.com
        url = 'https://api.ocr.space/parse/image'
        
        # Prepare the payload and headers
        payload = {
            'apikey': api_key,
            'language': 'eng' 
        }

        # Send the request with the image file
        response = requests.post(url, files={'file': image_file}, data=payload)

        # Handle the API response
        if response.status_code == 200:
            result = response.json()
            extracted_text = result['ParsedResults'][0]['ParsedText'] 

            # Save the text to a file
            text_filename = "converted_image_to_text.txt"
            text_path = os.path.join('media', text_filename)
            with open(text_path, 'w', encoding='utf-8') as f:
                f.write(extracted_text)

            # Provide file for download
            with open(text_path, 'r', encoding='utf-8') as f:
                response = HttpResponse(f, content_type='text/plain')
                response['Content-Disposition'] = f'attachment; filename={text_filename}'
                return response
        else:
            return HttpResponse("Error in OCR request: " + response.text, status=response.status_code)

    return render(request, 'App_Converter/image_to_text.html')


# ####### REMOVE BG ########
def remove_background(image_file):
    # Convert the image file into a format rembg can handle
    input_image = image_file.read()

    # Use rembg to remove the background
    output_image = remove(input_image)

    # Convert the output bytes into a BytesIO object
    output_image_io = BytesIO(output_image)

    # Open the image using PIL (ensure it's a PNG or other compatible format)
    image = Image.open(output_image_io)
    image = image.convert("RGBA")  # Ensure the image has an alpha channel

    # Save the image to an in-memory buffer as PNG
    buffered = BytesIO()
    image.save(buffered, format="PNG")

    # Return the in-memory file as Django's ContentFile
    return ContentFile(buffered.getvalue(), name="processed_image.png")

def upload_image(request):
    message = None
    processed_image_url = None  # To store the URL of the processed image
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image_instance = form.save(commit=False)

            # Process the image and remove background
            processed_image = remove_background(request.FILES['image'])

            # Save the processed image to the instance
            image_instance.processed_image.save(processed_image.name, processed_image)
            image_instance.save()

            # Set the URL of the processed image
            processed_image_url = image_instance.processed_image.url

            # Set a success message
            message = "Image has been successfully processed! You can download it below."

            # Reset the form for the user to upload another image
            form = ImageUploadForm()

    else:
        form = ImageUploadForm()

    return render(request, 'App_Converter/remove_background.html', {'form': form, 'message': message, 'processed_image_url': processed_image_url})

# ########### CONVERT IMAGE FORMAT ###########
def convert_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        target_format = request.POST.get('format').lower()  # Normalize format input to lowercase

        # Open the uploaded image
        image = Image.open(image_file)

        # If converting to JPEG, remove alpha channel by converting to RGB
        if target_format in ['jpeg', 'jpg']:
            if image.mode == 'RGBA':  # Check if image has an alpha channel
                image = image.convert('RGB')  # Convert to RGB to remove alpha channel
            target_format = 'JPEG'  # Normalize to 'JPEG' for PIL

        # Handle other formats
        if target_format == 'png':
            target_format = 'PNG'
        elif target_format == 'webp':
            target_format = 'WEBP'

        # Save the image to an in-memory file
        image_io = io.BytesIO()
        image.save(image_io, format=target_format.upper())  # Use the correct format
        image_io.seek(0)

        # Prepare the response for file download
        response = HttpResponse(image_io, content_type=f'image/{target_format.lower()}')
        response['Content-Disposition'] = f'attachment; filename=converted_image.{target_format.lower()}'
        return response

    return render(request, 'App_Converter/convert_image.html')

# Password Saver
key = Fernet.generate_key()
cipher = Fernet(key)

def save_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        encrypted_password = cipher.encrypt(password.encode())
        # Save encrypted_password to database or return to the user
        return JsonResponse({'encrypted_password': encrypted_password.decode()})
    return render(request, 'App_Converter/save_password.html')

# encrypt_password
def encrypt_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        encrypted_password = cipher.encrypt(password.encode())
        return JsonResponse({'encrypted_password': encrypted_password.decode()})
    return render(request, 'App_Converter/encrypt_password.html')

# decrypt_password
def decrypt_password(request):
    if request.method == 'POST':
        encrypted_password = request.POST['encrypted_password']
        decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
        return JsonResponse({'decrypted_password': decrypted_password})
    return render(request, 'App_Converter/decrypt_password.html')


# # Doc To PDF
# def doc_to_pdf(request):
#     if request.method == 'POST':
#         doc_file = request.FILES['doc']
#         document = Document(doc_file)
#         content = ""
#         for paragraph in document.paragraphs:
#             content += paragraph.text
#         pdf_file = HTML(string=content).write_pdf()
#         with open('output.pdf', 'wb') as f:
#             f.write(pdf_file)
#         return JsonResponse({'message': 'DOC converted to PDF', 'file': 'output.pdf'})
#     return render(request, 'App_Converter/doc_to_pdf.html')

#  mp4 to mp3
def mp4_to_mp3(request):
    if request.method == 'POST':
        video_file = request.FILES['video']
        audio = AudioSegment.from_file(video_file, format="mp4")
        output_filename = "audio.mp3"
        audio.export(output_filename, format="mp3")
        return JsonResponse({'message': 'MP4 converted to MP3', 'file': output_filename})
    return render(request, 'App_Converter/mp4_to_mp3.html')

# YT downlaoder
def download_yt(request):
    if request.method == "POST":
        form = DownloadForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            try:
                ydl_opts = {
                    'outtmpl': 'downloads/%(title)s.%(ext)s',
                    'quiet': True,
                }
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=True)
                    file_path = ydl.prepare_filename(info)

                # Return the file for download
                with open(file_path, 'rb') as f:
                    response = HttpResponse(f.read(), content_type="application/octet-stream")
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    return response
            except Exception as e:
                return render(request, 'App_Converter/error.html', {'error': str(e)})

    else:
        form = DownloadForm()

    return render(request, 'App_Converter/yt_downloader.html', {'form': form})





