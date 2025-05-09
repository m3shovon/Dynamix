from django.shortcuts import render
from django.http import JsonResponse
# from weasyprint import HTML
import json
import requests
import fitz  
from django.http import HttpResponse
import os
from PIL import Image
import io
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from .forms import ImageUploadForm, DownloadForm, QRCodeForm
from .models import ImageUpload, DownloadHistory, QRCode
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

# from rembg import remove


from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

from cryptography.fernet import Fernet
from docx import Document
from pydub import AudioSegment
from yt_dlp import YoutubeDL
import qrcode
import re
import socket
from whois import whois
from urllib.parse import urlparse
import dns.resolver

from Wappalyzer import Wappalyzer, WebPage

import logging

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'App_Converter/home.html')

# PDF TO Text
def pdf_to_text(request):
    if request.method == 'POST':
        pdf_file = request.FILES['pdf']
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            text = ""
            for page in doc:
                text += page.get_text()

        text_filename = "converted_pdf_to_text.txt"
        text_path = os.path.join('media', text_filename)
        
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
        api_key = 'K81007853788957'  # connected with: testnetworkeverything@gmail.com
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
    """
    Improved background removal function with better memory management
    and error handling.
    """
    try:
        # Process in chunks to reduce memory usage
        input_image = b''
        for chunk in image_file.chunks():
            input_image += chunk

        # Lazy import of rembg to reduce initial memory load
        from rembg import remove
        
        # Process the image
        output_image = remove(input_image)
        
        # Convert to PIL Image with memory optimization
        with BytesIO(output_image) as output_io:
            with Image.open(output_io) as image:
                image = image.convert("RGBA")
                
                # Save to buffer
                buffered = BytesIO()
                image.save(buffered, format="PNG", optimize=True)
                buffered.seek(0)
                
                return ContentFile(buffered.read(), name="processed_image.png")
                
    except Exception as e:
        logger.error(f"Background removal failed: {str(e)}")
        raise  # Re-raise the exception after logging

def validate_file_size(file):
    """Validate that the file size is within allowed limits"""
    if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
        raise ValidationError(
            f"File too large. Size should not exceed {settings.FILE_UPLOAD_MAX_MEMORY_SIZE/(1024*1024)}MB."
        )

def upload_image(request):
    message = None
    processed_image_url = None
    
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # Create but don't save to DB yet
                image_instance = form.save(commit=False)
                
                # Process the image
                processed_image = remove_background(request.FILES['image'])
                
                # Save the processed image
                image_instance.processed_image.save(
                    "processed_image.png", 
                    processed_image
                )
                image_instance.save()
                
                processed_image_url = image_instance.processed_image.url
                message = "Image processed successfully! Download below."
                
                # Reset form for new upload
                form = ImageUploadForm()
                
            except Exception as e:
                logger.error(f"Image processing error: {str(e)}")
                message = "Error processing image. Please try again."
    else:
        form = ImageUploadForm()

    return render(request, 'App_Converter/remove_background.html', {
        'form': form,
        'message': message,
        'processed_image_url': processed_image_url
    })

# def remove_background(image_file):
#     # Convert the image file into a format rembg can handle
#     input_image = image_file.read()

#     # Use rembg to remove the background
#     output_image = remove(input_image)

#     # Convert the output bytes into a BytesIO object
#     output_image_io = BytesIO(output_image)

#     # Open the image using PIL (ensure it's a PNG or other compatible format)
#     image = Image.open(output_image_io)
#     image = image.convert("RGBA") 

#     # Save the image to an in-memory buffer as PNG
#     buffered = BytesIO()
#     image.save(buffered, format="PNG")

#     # Return the in-memory file as Django's ContentFile
#     return ContentFile(buffered.getvalue(), name="processed_image.png")

# def upload_image(request):
#     message = None
#     processed_image_url = None  
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_instance = form.save(commit=False)

#             # Process the image and remove background
#             processed_image = remove_background(request.FILES['image'])

#             # Save the processed image to the instance
#             image_instance.processed_image.save(processed_image.name, processed_image)
#             image_instance.save()

#             # Set the URL of the processed image
#             processed_image_url = image_instance.processed_image.url
#             message = "Image has been successfully processed! You can download it below."

#             # Reset the form 
#             form = ImageUploadForm()

#     else:
#         form = ImageUploadForm()

#     return render(request, 'App_Converter/remove_background.html', {'form': form, 'message': message, 'processed_image_url': processed_image_url})

# ########### CONVERT IMAGE FORMAT ###########
def convert_image(request):
    if request.method == 'POST':
        image_file = request.FILES['image']
        target_format = request.POST.get('format').lower()  

        # Open the uploaded image
        image = Image.open(image_file)

        # If converting to JPEG, remove alpha channel by converting to RGB
        if target_format in ['jpeg', 'jpg']:
            if image.mode == 'RGBA':  
                image = image.convert('RGB')  
            target_format = 'JPEG' 

        # Handle other formats
        if target_format == 'png':
            target_format = 'PNG'
        elif target_format == 'webp':
            target_format = 'WEBP'

        # Saving the image to an in-memory file
        image_io = io.BytesIO()
        image.save(image_io, format=target_format.upper())
        image_io.seek(0)

        response = HttpResponse(image_io, content_type=f'image/{target_format.lower()}')
        response['Content-Disposition'] = f'attachment; filename=converted_image.{target_format.lower()}'
        return response

    return render(request, 'App_Converter/convert_image.html')
# Generate a key and initialize Fernet cipher
key = Fernet.generate_key()
cipher = Fernet(key)

# Password Saver
def save_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        encrypted_password = cipher.encrypt(password.encode())
        # Save encrypted_password to database or return to the user
        return JsonResponse({'encrypted_password': encrypted_password.decode()})
    return render(request, 'App_Converter/save_password.html')

# Encrypt Password
def encrypt_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        encrypted_password = cipher.encrypt(password.encode())
        return JsonResponse({'encrypted_password': encrypted_password.decode()})
    return render(request, 'App_Converter/encrypt_password.html')

# Decrypt Password
def decrypt_password(request):
    if request.method == 'POST':
        encrypted_password = request.POST['encrypted_password']
        try:
            decrypted_password = cipher.decrypt(encrypted_password.encode()).decode()
            return JsonResponse({'decrypted_password': decrypted_password})
        except Exception as e:
            return JsonResponse({'error': 'Invalid encrypted password'}, status=400)
    return render(request, 'App_Converter/decrypt_password.html')

# DOC to PDF Conversion
# def doc_to_pdf(request):
#     if request.method == 'POST':
#         doc_file = request.FILES['doc']
#         try:
#             document = Document(doc_file)
#             content = ""
#             for paragraph in document.paragraphs:
#                 content += f"<p>{paragraph.text}</p>"
#             pdf_file = HTML(string=content).write_pdf()

#             output_path = os.path.join('media', 'output.pdf')
#             with open(output_path, 'wb') as f:
#                 f.write(pdf_file)

#             return JsonResponse({'message': 'DOC converted to PDF', 'file': output_path})
#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)
#     return render(request, 'App_Converter/doc_to_pdf.html')

# MP4 to MP3 Conversion
def mp4_to_mp3(request):
    if request.method == 'POST':
        video_file = request.FILES['video']
        try:
            audio = AudioSegment.from_file(video_file, format="mp4")
            output_path = os.path.join('media', 'audio.mp3')
            audio.export(output_path, format="mp3")

            return JsonResponse({'message': 'MP4 converted to MP3', 'file': output_path})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
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

# Hash a password using PBKDF2
def hash_password(request):
    if request.method == 'POST':
        plain_password = request.POST['password']
        hashed_password = make_password(plain_password) 
        return JsonResponse({'hashed_password': hashed_password})
    return render(request, 'App_Converter/hash_password.html')

# Verify if the given password matches the hash
def verify_password(request):
    if request.method == 'POST':
        plain_password = request.POST['password']
        hashed_password = request.POST['hashed_password']
        is_valid = check_password(plain_password, hashed_password) 
        return JsonResponse({'is_valid': is_valid})
    return render(request, 'App_Converter/verify_password.html')

def generate_qr_code(request):
    qr_code_image_url = None  # Variable to hold the QR code image URL
    if request.method == 'POST':
        form = QRCodeForm(request.POST)
        if form.is_valid():
            qr_code_instance = form.save(commit=False)

            # Generate QR Code
            qr_image = qrcode.make(qr_code_instance.url)
            buffer = BytesIO()
            qr_image.save(buffer, format='PNG')

            # Sanitize file name
            sanitized_url = re.sub(r'[^\w\-_]', '_', qr_code_instance.url)
            file_name = f"{sanitized_url}.png"

            # Save the image to the model's ImageField
            qr_code_instance.qr_code_image.save(file_name, ContentFile(buffer.getvalue()), save=True)
            qr_code_instance.save()

            # Get the QR code image URL for rendering on the same page
            qr_code_image_url = qr_code_instance.qr_code_image.url
    else:
        form = QRCodeForm()

    return render(request, 'App_Converter/generate_qr_code.html', {'form': form, 'qr_code_image_url': qr_code_image_url})

# URL info Gatherer
def get_url_info(request):
    data = None
    error = None

    if request.method == "POST":
        url = request.POST.get('url')
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or parsed_url.path
            ip_address = socket.gethostbyname(domain)
            whois_info = whois(domain)
            
            open_ports = []
            common_ports = [80, 443, 21, 22, 25]
            for port in common_ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)  # 1-second timeout
                    result = sock.connect_ex((domain, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                except:
                    continue
            
            subdomains = []
            common_subdomains = ['www', 'mail', 'ftp', 'blog', 'api', 'test']
            for sub in common_subdomains:
                subdomain = f"{sub}.{domain}"
                try:
                    dns.resolver.resolve(subdomain, 'A')
                    subdomains.append(subdomain)
                except dns.resolver.NXDOMAIN:
                    continue
                except dns.resolver.NoAnswer:
                    continue
            
            data = {
                'domain': domain,
                'ip_address': ip_address,
                'whois_info': {
                    'registrar': whois_info.registrar,
                    'creation_date': whois_info.creation_date,
                    'expiration_date': whois_info.expiration_date,
                },
                'open_ports': open_ports,
                'subdomains': subdomains,
            }
        except Exception as e:
            error = f"Error fetching information: {str(e)}"

    return render(request, 'App_Converter/url_info.html', {'data': data, 'error': error})


# Website information gatherer
def analyze_website(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        wappalyzer = Wappalyzer.latest()
        webpage = WebPage.new_from_response(response)
        technologies = wappalyzer.analyze(webpage)

        # Convert the set to a list
        return {
            "status": "success",
            "url": url,
            "technologies": list(technologies),
        }

    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "message": str(e),
        }
    
# def analyze_website_view(request):
#     if request.method in ["POST", "GET"]:
#         url = request.POST.get("url") if request.method == "POST" else request.GET.get("url")
#         if not url:
#             return JsonResponse({"status": "error", "message": "URL is required."})

#         result = analyze_website(url)
#         return JsonResponse(result)

#     return JsonResponse({"status": "error", "message": "Invalid request method."})

def analyze_website_view(request):
    if request.method == "POST":
        url = request.POST.get("url")
        if not url:
            return render(request, "App_Converter/website_analyzer.html", {"error": "URL is required."})

        result = analyze_website(url)
        return render(request, "App_Converter/website_analyzer.html", {"result": result})

    return render(request, "App_Converter/website_analyzer.html")