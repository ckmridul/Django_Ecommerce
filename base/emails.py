from django.conf import settings
from django.core.mail import send_mail

 
def send_account_activation_email(email, email_otp):
    subject = 'Your accont needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    
    message = f'''Hi, 
    Please enter the below code to complte verification
    {email_otp}'''
    
    send_mail(subject, message, email_from, [email])