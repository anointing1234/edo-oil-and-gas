from django.shortcuts import render,get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse
import requests 
from decimal import Decimal, InvalidOperation
import logging
import json
from django.http import HttpResponseBadRequest
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime, timedelta, time
from django.http import Http404
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout,login as auth_login,authenticate
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Max
from decimal import Decimal,InvalidOperation
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.conf.urls.static import static
from django.core.mail import EmailMultiAlternatives
import pytz
from datetime import datetime, timedelta
from pytz import timezone as pytz_timezone
import logging
from django.contrib.auth.decorators import login_required
import logging
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password
from django.contrib.auth import logout
import string
import random
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import re


# Set up logging
logger = logging.getLogger(__name__)

def home(request):
    return render(request,'home/index.html')


def about(request):
    return render(request,'home/about.html')


def contact(request):
    return render(request,'home/contact.html')


def privacy_policy(request):
    return render(request,'home/privacy.html')


def reservation(request):
    return render(request,'home/reservation.html')


def sponsors(request):
    return render(request,'home/sponsors.html')

def exhibitors(request):
    return render(request,'home/exhibitors.html')




def reserve_seat(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        occupation = request.POST.get('occupation')
        company_name = request.POST.get('company_name')
        company_address = request.POST.get('company_address')

        # Server-side validation
        if not all([first_name, last_name, email, phone]):
            logger.warning(f"Invalid submission: Missing required fields - first_name: {first_name}, last_name: {last_name}, email: {email}, phone: {phone}")
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields.'})

        # Validate email format
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            logger.warning(f"Invalid email format: {email}")
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'})

        # Validate phone format (Nigerian numbers: +234 or 0 followed by 10 digits)
        phone_pattern = r'^\+234[0-9]{10}$|^0[0-9]{10}$'
        if not re.match(phone_pattern, phone):
            logger.warning(f"Invalid phone format: {phone}")
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid Nigerian phone number (e.g., +2348034715913 or 08034715913).'})

        # Prepare the email content with HTML formatting
        subject = 'New Seat Reservation – Edo State Oil and Gas Summit 2025'
        plain_message = f"""
New seat reservation submitted:
First Name: {first_name}
Last Name: {last_name}
Phone: {phone}
Email: {email}
Occupation: {occupation or 'N/A'}
Company Name: {company_name or 'N/A'}
Company Address: {company_address or 'N/A'}
"""
        html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f7; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 40px auto; background: #fff; border: 1px solid #ddd; padding: 30px;">
            <div style="text-align: center; border-bottom: 1px solid #e1e1e1; padding-bottom: 15px; margin-bottom: 25px;">
                <h1 style="color: #006838; margin: 0;">Edo State Oil and Gas Summit 2025</h1>
                <p style="font-size: 16px; color: #555;">Official Reservation Notification</p>
            </div>
            <p style="font-size: 15px; color: #333;">A new seat reservation has been submitted with the following details:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr><td style="padding: 8px; font-weight: bold; width: 30%;">First Name:</td><td style="padding: 8px;">{first_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Last Name:</td><td style="padding: 8px;">{last_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Phone:</td><td style="padding: 8px;">{phone}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Email:</td><td style="padding: 8px;">{email}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Occupation:</td><td style="padding: 8px;">{occupation or 'N/A'}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Company Name:</td><td style="padding: 8px;">{company_name or 'N/A'}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Company Address:</td><td style="padding: 8px;">{company_address or 'N/A'}</td></tr>
            </table>
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                This is an automated message from the Edo State Oil and Gas Summit reservation system.
            </p>
        </div>
    </body>
</html>
"""
        admin_email = 'info@edooilandgassummit.com'

        # Send email and handle failures gracefully
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin_email],
                html_message=html_message,
                fail_silently=True
            )
            logger.info(f"Reservation email sent to {admin_email} for {email}")
        except Exception as e:
            logger.error(f"Error sending reservation email to {admin_email}: {str(e)}")

        # Return success regardless of email outcome
        return JsonResponse({
            'status': 'success',
            'message': 'Congratulations! Your reservation to attend the Edo State Oil and Gas Summit has been received. Confirmation is currently pending — you will receive an email from us once your reservation is confirmed.'
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})

def contact_view(request):
    if request.method == 'POST':
        # Get form data
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message_body = request.POST.get('message')

        # Server-side validation
        if not all([first_name, last_name, email, phone, message_body]):
            logger.warning(f"Invalid contact submission: Missing required fields - first_name: {first_name}, last_name: {last_name}, email: {email}, phone: {phone}, message: {message_body}")
            return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields.'})

        # Validate email format
        email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_pattern, email):
            logger.warning(f"Invalid email format: {email}")
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid email address.'})

        # Validate phone format
        phone_pattern = r'^\+234[0-9]{10}$|^0[0-9]{10}$'
        if not re.match(phone_pattern, phone):
            logger.warning(f"Invalid phone format: {phone}")
            return JsonResponse({'status': 'error', 'message': 'Please provide a valid Nigerian phone number (e.g., +2348034715913 or 08034715913).'})

        # Prepare the email content
        subject = 'New Contact Message – Edo Oil & Gas Summit 2025'
        plain_message = f"""
            New contact message submitted:
            First Name: {first_name}
            Last Name: {last_name}
            Email: {email}
            Phone: {phone}
            Message: {message_body}
            """
        html_message = f"""
<html>
    <body style="font-family: Arial, sans-serif; background-color: #f4f6f7; margin: 0; padding: 0;">
        <div style="max-width: 700px; margin: 40px auto; background: #fff; border: 1px solid #ddd; padding: 30px;">
            <div style="text-align: center; border-bottom: 1px solid #e1e1e1; padding-bottom: 15px; margin-bottom: 25px;">
                <h1 style="color: #006838; margin: 0;">Edo State Oil and Gas Summit 2025</h1>
                <p style="font-size: 16px; color: #555;">New Contact Submission</p>
            </div>
            <p style="font-size: 15px; color: #333;">A new message has been submitted through the contact form:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
                <tr><td style="padding: 8px; font-weight: bold;">First Name:</td><td style="padding: 8px;">{first_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Last Name:</td><td style="padding: 8px;">{last_name}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Email:</td><td style="padding: 8px;">{email}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Phone:</td><td style="padding: 8px;">{phone}</td></tr>
                <tr><td style="padding: 8px; font-weight: bold;">Message:</td><td style="padding: 8px;">{message_body}</td></tr>
            </table>
            <p style="margin-top: 30px; font-size: 14px; color: #666;">
                This is an automated message from the Edo Oil and Gas Summit website.
            </p>
        </div>
    </body>
</html>
"""
        admin_email = 'info@edooilandgassummit.com'

        # Send email and handle failures gracefully
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[admin_email],
                html_message=html_message,
                fail_silently=True
            )
            logger.info(f"Contact email sent to {admin_email} from {email}")
        except Exception as e:
            logger.error(f"Error sending contact email to {admin_email}: {str(e)}")

        # Return success regardless of email outcome
        return JsonResponse({
            'status': 'success',
            'message': 'Your message has been received. We will get back to you soon.'
        })

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'})