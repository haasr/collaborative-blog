from django.shortcuts import render

from .models import EmailSubscriber

def unsubscribe(request, email):
    sub = EmailSubscriber.objects.get(email_addr=email)
    sub.delete()
    return render(request, 'site_pages/unsubscribed.html', {})