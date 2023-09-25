from django.core.mail import send_mail
from django.conf import settings
from .models import User

def send_email(data):
    subject = f'Your registration email'
    
    email_from = settings.EMAIL_HOST
    send_mail(subject,data['message'], email_from, [data['email']])
    user_obj = User.objects.get(email=data['email'])
    user_obj.save()