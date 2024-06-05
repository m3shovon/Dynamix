from django.core.mail import send_mail
from django.conf import settings

def send_mail_to_client():
    subject = 'Testing Email'
    message = 'This is test email'
    from_email = settings.EMAIL_HOST_USER
    to_email = ["laila.cse51@gmail.com"]
    send_mail(subject, message, from_email, to_email)