from admin_pages.models import AuthorProfile, EmailContactFormSettings, SiteLook, SEO, SubscribeFormSettings
from site_pages_forms.forms import *
from blog import settings
from two_factor import utils as twofactor_utils

def add_to_context(request):
    site_look = SiteLook.objects.get(id=1)
    seo = SEO.objects.get(id=1)
    emailcontactform_settings = EmailContactFormSettings.objects.get(id=1)
    subscribeform_settings = SubscribeFormSettings.objects.get(id=1)
    try:
        f = site_look.font.split('&&')
    except:
        f[0] = '<link href="https://fonts.googleapis.com/css2?family=Mulish&display=swap" rel="stylesheet">'
        f[1] = "Mulish"

    profile = None
    if request.user.is_authenticated:
        profile = AuthorProfile.objects.get(user=request.user)

    return {
        'meta_title': seo.meta_title,
        'meta_description': seo.meta_description,
        'meta_author': seo.meta_author,
        'meta_keywords': seo.meta_keywords,
        'robots_index': seo.robots_index,
        'robots_follow': seo.robots_follow,

        'email_contact_form': EmailContactForm(),
        'email_contact_form_settings': emailcontactform_settings,
        'subscribe_form': EmailSubscriberForm(),
        'subscribe_form_settings': subscribeform_settings,

        'show_home': site_look.show_home,
        'show_topics': site_look.show_topics,
        'show_timeline': site_look.show_timeline,
        'show_contact': site_look.show_contact,
        'show_contrib': site_look.show_contrib,
        'show_about': site_look.show_about,
        'footer_copyright': site_look.footer_copyright,
        'footer_tagline': site_look.footer_tagline,
        'footer_about': site_look.footer_about,
        'footer_location': site_look.footer_location,
        'navigation_img_size': site_look.navigation_img_size,
        'footer_lat': site_look.lat,
        'footer_lon': site_look.lon,
        'footer_color': site_look.footer_color,
        'footer_contact_email': site_look.footer_contact_email,
        'footer_contact_phone': site_look.footer_contact_phone,
        'navigation_img_size': site_look.navigation_img_size,
        'font': f[0],
        'font_family': f[1],
        'footer_text_color': site_look.footer_text_color,
        'tinymce_script': settings.TINYMCE_SCRIPT,

        'profile': profile,

        'twofactor_default_device': twofactor_utils.default_device(request.user)
    }
