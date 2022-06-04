from admin_pages.models import EmailAccount
from django.core.mail import EmailMessage
from admin_pages.models import Contact, Contrib, EmailContactFormSettings, FormSendFailure, SubscriberNewsletter, SubscribeFormSettings
from anymail.exceptions import *

from threading import Thread


recip_email_acct = EmailAccount.objects.get(id=1)
contact = Contact.objects.get(id=1)
contrib = Contrib.objects.get(id=1)
email_contact_form_settings = EmailContactFormSettings.objects.get(id=1)
subscriber_newsletter = SubscriberNewsletter.objects.get(id=1)
subscribeform_settings = SubscribeFormSettings.objects.get(id=1)


class FormSender:
    form_failures = {}
    f_id = -2147483648


    def stash_failure(to, form_name, formdata):
        try:
            FormSender.f_id +=1
        except: # Int range exceeded
            FormSender.f_id = -2147483648
        f = FormSendFailure(
                to=to,
                form_name=form_name,
                exception='Uncaptured',
                # Truncate to fit model max (will have to try to eval to dict since truncated will fail)
                form_data=str(formdata)[:600]
        )
        FormSender.form_failures[FormSender.f_id] = f
        return FormSender.f_id


    def save_failure(id, ex='None'):
        f = FormSender.form_failures.pop(id)
        f.exception = str(ex)[:500] # Truncate to fit model max
        f.save()


    def send(to, form_name, formdata, message, save_failure=True):
        f_id = FormSender.stash_failure(to, form_name, formdata)
        success = 0
        try:
            message.send(fail_silently=False)
            FormSender.form_failures.pop(f_id)
            success = 1
        except (AnymailRequestsAPIError, AnymailRecipientsRefused, AnymailInvalidAddress,
            AnymailSerializationError, AnymailUnsupportedFeature) as ex:
            success = 0
            if save_failure:
                FormSender.save_failure(f_id, ex)
        except Exception as ex:
            success = 0
            if save_failure:
                FormSender.save_failure(f_id, ex)
        try:
            FormSender.form_failures.pop(f_id)
        except: # Already popped
            pass

        return success


def get_email_recipient():
    global recip_email_acct
    recip_email_acct.refresh_from_db()
    return recip_email_acct.email_addr


def resend_form_email(form_data, to, form_name):
    message = EmailMessage(to=[to])
    if form_name == 'Subscribe':
        subscribeform_settings.refresh_from_db()
        message.template_id = subscribeform_settings.subscribed_mail_template_id
    elif form_name == 'Email Contact':
        email_contact_form_settings.refresh_from_db()
        message.template_id = email_contact_form_settings.mail_template_id
    elif form_name == 'Contact':
        contact.refresh_from_db()
        message.template_id = contact.contact_mail_template_id
    elif form_name == 'Contrib':
        contrib.refresh_from_db()
        message.template_id = contrib.mail_template_id

    message.from_email = None
    message.merge_global_data = form_data
    return FormSender.send(message.to[0], form_name, form_data, message)


def send_subscribe_email(time, email, first_name, last_name=''):
    title = "You've subscribed"
    msg = (
        f"{first_name}, you have subscribed to receive newsletters."
        f" You may unsubscribe at any time using the provided link."
    )

    formdata = {
        'title': title,
        'message': msg,
        'unsubscribe_url': f"{subscriber_newsletter.unsubscribe_url}{email}"
    }

    subscribeform_settings.refresh_from_db()
    message = EmailMessage(to=[email])
    message.template_id = subscribeform_settings.subscribed_mail_template_id
    message.from_email = None
    message.merge_global_data = formdata

    return FormSender.send(email, 'Subscribe', formdata, message)


def send_contact_email(time, contact_email):
    """Sends an email to the recipient timestamped with the value of
    the param, time and a message pertaining to and including the
    form data -- which in this case is simply an email address of
    someone who would like information about the church.

    Parameters:
    time (str): A timestamp in the format '%m/%d/%y %I:%M %p' (see datetime documentation).
    contact_email (str): A contact email address from a submitted form's data.
    """
    title = "New Email Contact - " + time
    msg = f"{contact_email} has contacted you to find out more about Ryan's Reflections."

    formdata = {
        'title': title,
        'message': msg,
    }

    email_contact_form_settings.refresh_from_db()
    message = EmailMessage(to=[get_email_recipient()])
    message.template_id = email_contact_form_settings.mail_template_id
    message.from_email = None
    message.merge_global_data = formdata

    FormSender.send(message.to[0], 'Email Contact', formdata, message)


def send_contact_form(time, name, email, comment):
    """Sends an email to the recipient timestamped with the value of
    the param, time, and a message pertaining to and including the
    form data -- which in this case is a name and a comment from
    someone.

    Parameters:
    time (str): A timestamp in the format '%m/%d/%y %I:%M %p' (see datetime documentation).
    name (str): A name from a submitted form's data.
    comment (str): A comment from a submitted form's data.
    """
    title = "New Contact - " + time

    formdata = {
        'title': title,
        'name': name,
        'email': email,
        'comment': comment
    }

    message = EmailMessage(to=[get_email_recipient()])
    contact.refresh_from_db()
    message.template_id = contact.contact_mail_template_id
    message.from_email = None
    message.merge_global_data = formdata

    FormSender.send(message.to[0], 'Contact', formdata, message)


def send_contrib_form(time, name, email, username, about):
    """Sends an email to the recipient timestamped with the value of
    the param, time, and a message pertaining to and including the
    form data -- which in this case is a name and a short about
    description from someone.

    Parameters:
    time (str): A timestamp in the format '%m/%d/%y %I:%M %p' (see datetime documentation).
    name (str): A name from a submitted form's data.
    comment (str): A comment from a submitted form's data.
    """

    title = "New Contrib Request - " + time

    formdata = {
        'title': title,
        'name': name,
        'email': email,
        'about': about,
        'desired_username': username
    }

    message = EmailMessage(to=[get_email_recipient()])

    contrib.refresh_from_db()
    message.template_id = contrib.contrib_mail_template_id
    message.from_email = None
    message.merge_global_data = formdata

    FormSender.send(message.to[0], 'Contrib', formdata, message)
