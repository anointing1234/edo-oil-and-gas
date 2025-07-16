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

        # Validate message content for unwanted topics (case-insensitive)
        restricted_keywords = [
            'website', 'web development', 'web design', 'site development',
            'mobile app', 'app development', 'application development',
            'seo', 'search engine optimization', 'search optimization',
            'digital marketing', 'web optimization'
        ]
        message_lower = message_body.lower()
        for keyword in restricted_keywords:
            if keyword in message_lower:
                logger.warning(f"Invalid message content: Contains restricted keyword '{keyword}'")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Messages about website development, mobile apps, or SEO are not accepted. Please submit inquiries related to oil and gas.'
                })

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
  
  


def send_message(request):
       return render(request,'home/email_message.html')
     
     
     
def decline(request):
  return render(request,'home/decline.html')     




def send_messages(request):
    if request.method == 'POST':
        try:
            # Extract form data
            email = request.POST.get('email', '').strip()
            message = request.POST.get('message', '').strip()

            # Validate email format
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, email):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email address.'
                }, status=400)

            # Validate message
            if not message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message cannot be empty.'
                }, status=400)

            if len(message) > 1000:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message is too long. Maximum length is 1000 characters.'
                }, status=400)

            # Context for email
            context = {
                'attendee_email': email,
                'organizer_message': message,
                'event_name': 'Edo Oil & Gas Summit 2025',
                'event_location': 'Victor Uwaifo Creative Hub, Along Airport Road, Benin City, Edo State',
                'event_date': 'August 7, 2005',
                'contact_email': 'info@edooilandgassummit.com',
                'contact_phone1': '+234 803 471 5913',
                'contact_phone2': '+234 806 442 5068',
                'logo_url': 'http://edooilandgassummit.com/static/images/logo.png'  # Update for production
            }

            # HTML email content
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Edo Oil & Gas Summit 2025 - Seat Reservation Confirmation</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
      line-height: 1.6;
      color: #1a2b3c;
      background-color: #f9fafb;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }}
    .header {{
      text-align: center;
      padding: 20px 0;
      background: linear-gradient(135deg, #ffd700, #ffed4e);
      border-radius: 8px 8px 0 0;
    }}
    .header img {{
      max-width: 150px;
      height: auto;
    }}
    .content {{
      padding: 30px;
    }}
    .content h1 {{
      font-size: 24px;
      color: #1a2b3c;
      margin-bottom: 20px;
    }}
    .content p {{
      font-size: 16px;
      color: #374151;
      margin-bottom: 15px;
    }}
    .content .message-box {{
      background-color: #f3f4f6;
      padding: 20px;
      border-left: 4px solid #ffd700;
      margin: 20px 0;
      border-radius: 4px;
    }}
    .event-details {{
      background-color: #f9fafb;
      padding: 20px;
      border-radius: 4px;
      margin: 20px 0;
    }}
    .event-details h2 {{
      font-size: 18px;
      color: #1a2b3c;
      margin-bottom: 15px;
    }}
    .event-details ul {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .event-details li {{
      font-size: 16px;
      color: #374151;
      margin-bottom: 10px;
    }}
    .event-details li strong {{
      color: #1a2b3c;
    }}
    .footer {{
      text-align: center;
      padding: 20px;
      background-color: #1f2937;
      color: #d1d5db;
      border-radius: 0 0 8px 8px;
      font-size: 14px;
    }}
    .footer a {{
      color: #ffd700;
      text-decoration: none;
    }}
    .footer a:hover {{
      text-decoration: underline;
    }}
    .contact-info {{
      margin-top: 20px;
    }}
    .contact-info p {{
      margin: 5px 0;
    }}
    .button {{
      display: inline-block;
      padding: 12px 24px;
      background: linear-gradient(135deg, #ffd700, #ffed4e);
      color: #1a2b3c;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 600;
      margin-top: 20px;
    }}
    .button:hover {{
      background: linear-gradient(135deg, #ffed4e, #ffd700);
    }}
    @media only screen and (max-width: 600px) {{
      .container {{
        padding: 10px;
      }}
      .header img {{
        max-width: 120px;
      }}
      .content h1 {{
        font-size: 20px;
      }}
      .content p, .event-details li {{
        font-size: 14px;
      }}
      .footer {{
        font-size: 12px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="{context['logo_url']}" alt="Edo Oil & Gas Summit 2025 Logo">
    </div>
    <div class="content">
      <h1>Seat Reservation Confirmation</h1>
      <p>Dear Attendee,</p>
      <p>Thank you for reaching out to us to get a reservation seat for the <strong>{context['event_name']}</strong>. We are delighted to confirm your participation in this landmark event driving innovation and growth in Edo State's energy sector.</p>
      <div class="message-box">
        <p><strong>Message from the Organizers:</strong></p>
        <p>{context['organizer_message']}</p>
      </div>
      <div class="event-details">
        <h2>Event Details</h2>
        <ul>
          <li><strong>Event:</strong> {context['event_name']}</li>
          <li><strong>Location:</strong> {context['event_location']}</li>
          <li><strong>Date:</strong> {context['event_date']}</li>
        </ul>
      </div>
      <p>For any inquiries, please contact us at <a href="mailto:{context['contact_email']}">{context['contact_email']}</a> or call <a href="tel:{context['contact_phone1']}">{context['contact_phone1']}</a> or <a href="tel:{context['contact_phone2']}">{context['contact_phone2']}</a>.</p>
      <a href="http://edooilandgassummit.com" class="button">Learn More About the Summit</a>
    </div>
    <div class="footer">
      <p>Best regards,<br>Edo Oil & Gas Summit Team</p>
      <div class="contact-info">
        <p><a href="mailto:{context['contact_email']}">{context['contact_email']}</a></p>
        <p><a href="https://tslnigeria.com">tslnigeria.com</a></p>
      </div>
      <p>© 2025 Edo Oil & Gas Summit. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""

            # Plain text version for fallback
            text_content = f"""
Dear Attendee,

Thank you for reserving your seat for the Edo Oil & Gas Summit 2025. We are pleased to confirm your participation in this landmark event.

Message from the Organizers:
{message}

Event Details:
- Event: Edo Oil & Gas Summit 2025
- Location: Victor Uwaifo Creative Hub, Along Airport Road, Benin City, Edo State
- Date: August 7, 2025

For any inquiries, please contact us at info@edooilandgassummit.com or call +234 803 471 5913 or +234 806 442 5068.

Best regards,
Edo Oil & Gas Summit Team
"""

            # Send confirmation email to the attendee
            subject = 'Edo Oil & Gas Summit 2025 - Seat Reservation Confirmation'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list,
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)

            # Optionally notify organizers (commented out as per your code)
            """
            organizer_subject = 'Sent Confirmation for Edo Oil & Gas Summit 2025 Reservation'
            organizer_body = f'''
A confirmation message was sent to an attendee for the Edo Oil & Gas Summit 2025.

Attendee Email: {email}
Message Sent:
{message}
'''
            send_mail(
                subject=organizer_subject,
                message=organizer_body,
                from_email=from_email,
                recipient_list=['info@edooilandgassummit.com'],
                fail_silently=True,
            )
            """

            return JsonResponse({
                'status': 'success',
                'message': 'Confirmation message sent successfully to the attendee!'
            })

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while sending the confirmation message. Please try again later.'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)
    
    
    
    



def decline_message(request):
    if request.method == 'POST':
        try:
            # Extract form data
            email = request.POST.get('email', '').strip()
            message = request.POST.get('message', '').strip()

            # Validate email format
            email_pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            if not re.match(email_pattern, email):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email address.'
                }, status=400)

            # Validate message
            if not message:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message cannot be empty.'
                }, status=400)

            if len(message) > 1000:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Message is too long. Maximum length is 1000 characters.'
                }, status=400)

            # Context for email
            context = {
                'attendee_email': email,
                'organizer_message': message,
                'event_name': 'Edo Oil & Gas Summit 2025',
                'event_location': 'Victor Uwaifo Creative Hub, Along Airport Road, Benin City, Edo State',
                'event_date': 'August 7, 2025',
                'contact_email': 'info@edooilandgassummit.com',
                'contact_phone1': '+234 803 471 5913',
                'contact_phone2': '+234 806 442 5068',
                'logo_url': 'http://edooilandgassummit.com/static/images/logo.png'  # Update for production
            }

            # HTML email content
            html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Edo Oil & Gas Summit 2025 - Seat Reservation Decline</title>
  <style>
    body {{
      margin: 0;
      padding: 0;
      font-family: 'Segoe UI', Arial, sans-serif;
      line-height: 1.6;
      color: #1a2b3c;
      background-color: #f9fafb;
    }}
    .container {{
      max-width: 600px;
      margin: 0 auto;
      padding: 20px;
      background-color: #ffffff;
      border-radius: 8px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }}
    .header {{
      text-align: center;
      padding: 20px 0;
      background: linear-gradient(135deg, #ffd700, #ffed4e);
      border-radius: 8px 8px 0 0;
    }}
    .header img {{
      max-width: 150px;
      height: auto;
    }}
    .content {{
      padding: 30px;
    }}
    .content h1 {{
      font-size: 24px;
      color: #1a2b3c;
      margin-bottom: 20px;
    }}
    .content p {{
      font-size: 16px;
      color: #374151;
      margin-bottom: 15px;
    }}
    .content .message-box {{
      background-color: #f3f4f6;
      padding: 20px;
      border-left: 4px solid #ffd700;
      margin: 20px 0;
      border-radius: 4px;
    }}
    .event-details {{
      background-color: #f9fafb;
      padding: 20px;
      border-radius: 4px;
      margin: 20px 0;
    }}
    .event-details h2 {{
      font-size: 18px;
      color: #1a2b3c;
      margin-bottom: 15px;
    }}
    .event-details ul {{
      list-style: none;
      padding: 0;
      margin: 0;
    }}
    .event-details li {{
      font-size: 16px;
      color: #374151;
      margin-bottom: 10px;
    }}
    .event-details li strong {{
      color: #1a2b3c;
    }}
    .footer {{
      text-align: center;
      padding: 20px;
      background-color: #1f2937;
      color: #d1d5db;
      border-radius: 0 0 8px 8px;
      font-size: 14px;
    }}
    .footer a {{
      color: #ffd700;
      text-decoration: none;
    }}
    .footer a:hover {{
      text-decoration: underline;
    }}
    .contact-info {{
      margin-top: 20px;
    }}
    .contact-info p {{
      margin: 5px 0;
    }}
    .button {{
      display: inline-block;
      padding: 12px 24px;
      background: linear-gradient(135deg, #ffd700, #ffed4e);
      color: #1a2b3c;
      text-decoration: none;
      border-radius: 4px;
      font-weight: 600;
      margin-top: 20px;
    }}
    .button:hover {{
      background: linear-gradient(135deg, #ffed4e, #ffd700);
    }}
    @media only screen and (max-width: 600px) {{
      .container {{
        padding: 10px;
      }}
      .header img {{
        max-width: 120px;
      }}
      .content h1 {{
        font-size: 20px;
      }}
      .content p, .event-details li {{
        font-size: 14px;
      }}
      .footer {{
        font-size: 12px;
      }}
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <img src="{context['logo_url']}" alt="Edo Oil & Gas Summit 2025 Logo">
    </div>
    <div class="content">
      <h1>Seat Reservation Decline</h1>
      <p>Dear Attendee,</p>
      <p>We regret to inform you that your reservation request for the <strong>{context['event_name']}</strong> has not been approved at this time.</p>
      <div class="message-box">
        <p><strong>Message from the Organizers:</strong></p>
        <p>{context['organizer_message']}</p>
      </div>
      <div class="event-details">
        <h2>Event Details</h2>
        <ul>
          <li><strong>Event:</strong> {context['event_name']}</li>
          <li><strong>Location:</strong> {context['event_location']}</li>
          <li><strong>Date:</strong> {context['event_date']}</li>
        </ul>
      </div>
      <p>For any inquiries, please contact us at <a href="mailto:{context['contact_email']}">{context['contact_email']}</a> or call <a href="tel:{context['contact_phone1']}">{context['contact_phone1']}</a> or <a href="tel:{context['contact_phone2']}">{context['contact_phone2']}</a>.</p>
      <a href="http://edooilandgassummit.com" class="button">Learn More About the Summit</a>
    </div>
    <div class="footer">
      <p>Best regards,<br>Edo Oil & Gas Summit Team</p>
      <div class="contact-info">
        <p><a href="mailto:{context['contact_email']}">{context['contact_email']}</a></p>
        <p><a href="https://tslnigeria.com">tslnigeria.com</a></p>
      </div>
      <p>© 2025 Edo Oil & Gas Summit. All rights reserved.</p>
    </div>
  </div>
</body>
</html>
"""

            # Plain text version for fallback
            text_content = f"""
Dear Attendee,

We regret to inform you that your reservation request for the Edo Oil & Gas Summit 2025 has not been approved at this time.

Message from the Organizers:
{message}

Event Details:
- Event: Edo Oil & Gas Summit 2025
- Location: Victor Uwaifo Creative Hub, Along Airport Road, Benin City, Edo State
- Date: August 7, 2025

For any inquiries, please contact us at info@edooilandgassummit.com or call +234 803 471 5913 or +234 806 442 5068.

Best regards,
Edo Oil & Gas Summit Team
"""

            # Send decline email to the attendee
            subject = 'Edo Oil & Gas Summit 2025 - Seat Reservation Decline'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [email]

            email_message = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=recipient_list,
            )
            email_message.attach_alternative(html_content, "text/html")
            email_message.send(fail_silently=False)

            # Optionally notify organizers
            """
            organizer_subject = 'Sent Decline for Edo Oil & Gas Summit 2025 Reservation'
            organizer_body = f'''
A decline message was sent to an attendee for the Edo Oil & Gas Summit 2025.

Attendee Email: {email}
Message Sent:
{message}
'''
            send_mail(
                subject=organizer_subject,
                message=organizer_body,
                from_email=from_email,
                recipient_list=['info@edooilandgassummit.com'],
                fail_silently=True,
            )
            """

            return JsonResponse({
                'status': 'success',
                'message': 'Decline message sent successfully to the attendee!'
            })

        except Exception as e:
            logger.error(f"Error sending email: {str(e)}", exc_info=True)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while sending the decline message. Please try again later.'
            }, status=500)

    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    }, status=405)