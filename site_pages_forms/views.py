from django.http import HttpResponse

from datetime import datetime as dt

from admin_pages.models import DenylistEmail
from mail_subscription.models import EmailSubscriber
from . import form_sender

import threading

def get_current_time():
    now = dt.now()
    return dt.strftime(now, '%m/%d/%y %I:%M %p')


def send_form(email):
    """Checks the email denylist to see if the string received in the
    email param matches any email address in the list.

    Parameters:
    email (str): An email address.

    Returns:
    send (bool): True if the arg received did not match any item in the list and False otherwise.
    """
    email_denylist = DenylistEmail.objects.all().values_list('email_addr', flat=True)
    send = True
    for email_addr in email_denylist:
        if (email_addr==email):
            send = False
            break
    return send


def submit_subscribe_form(request):
    """If the form was submitted as a POST request
    and the email in the form data is not on the
    email denylist and the email has not already been
    used in an existing EmailSubscriber object, a new
    EmailSubscriber is created using the form data and
    the data is passed to the form_sender module's send_subscribe_form
    function to email a confirmation to the subscriber.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if request.method == 'POST':
        now = get_current_time()
        email = request.POST['sub_email']

        if send_form(email):
            fname = request.POST['fname']
            lname = request.POST['lname']
            subs = EmailSubscriber.objects.filter(email_addr=email)
            if len(subs) == 0: # Else, it is already stored
                sub = EmailSubscriber(
                    first_name=fname,
                    last_name=lname,
                    email_addr=email
                )
                sub.save() # Add entry in the DB

                t = threading.Thread(
                    target=form_sender.send_subscribe_email,
                    args=(now, email, fname, lname)
                )
                t.start()
            return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def sumbit_contact_form(request):
    """If the form was submitted as a POST request
    and the email in the form data is not on the
    email denylist, the form data is passed to
    the form_sender module's send_contact_form
    function to email the data to the recipient
    specified by the admin_pages.models.EmailAccount
    object with id 1.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if (request.method == 'POST'):
        now = get_current_time()
        email = request.POST['email']
        if (send_form(email)):
            name = (request.POST['fname'] + ' ' +
                    request.POST['lname'])

            t = threading.Thread(target=form_sender.send_contact_form,
                                args=(now, name, email, request.POST['comment'],))
            t.start()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def submit_contrib_form(request):
    """If the form was submitted as a POST request
    and the email in the form data is not on the
    email denylist, the form data is passed to
    the form_sender module's send_contrib_form
    function to email the data to the recipient
    specified by the admin_pages.models.EmailAccount
    object with id 1.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if (request.method == 'POST'):
        now = get_current_time()
        email = request.POST.get('email')
        if send_form(email):
            name = (request.POST['fname'] + ' ' +
                    request.POST['lname'])

            t = threading.Thread(target=form_sender.send_contrib_form,
                                args=(now, name, email, request.POST['uname'],
                                     request.POST['about'],))
            t.start()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)


def submit_contact_email(request):
    """If the form was submitted as a POST request
    and the email in the form data is not on the
    email denylist, the form data is passed to
    the form_sender module's send_contact_form
    function to email the data to the recipient
    specified by the admin_pages.models.EmailAccount
    object with id 1.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Returns the status which will Ajax will use to display a Javascript alert.
    """
    if (request.method == 'POST'):
        now = get_current_time()
        email = request.POST.get('viewer_email')
        if(send_form(email)):
            t = threading.Thread(target=form_sender.send_contact_email,
                                args=(now, email,))
            t.start()
        return HttpResponse(status=200) # Return a 200 even if the email addr is blocked.
    else:
        return HttpResponse(status=403)