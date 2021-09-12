from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Newsletter
import datetime
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
import random
import math
from django.contrib.auth.hashers import make_password


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


def newsletter(request):
    if request.method == "POST":
        email = request.POST["newsletter_email"]

        if Newsletter.objects.filter(email=email).exists():
            messages.info(request, "You are already a part of our Newletter Subscribers!")
            return redirect("index")
        else:
            email_save = Newsletter.objects.create(email=email)
            email_save.save()
            subject = 'Thank You for Subscribing to Affiliator.in Newsletter!'
            message = 'Hey There!\n\nThank You for subscribing to the Affiliator.in Newsletter.\n\nTo stay up to date with Affiliator.in services and Management Theories, Learn new tactics about how to earn more Affiliate Income with Affiliator.in.\n\nThank You\nTeam Affiliator.in '
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject, message, from_email, to_list, fail_silently=True)
            messages.info(request,"Thanks for subscribing to Affiliator.in Newsletter!")
            return redirect("index")

    else:
        return redirect("index")