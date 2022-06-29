from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from colorfield.fields import ColorField
from .models_options import *
import os
from functools import partial

# _update and _upload functions from https://newbedev.com/how-to-change-the-file-name-of-an-uploaded-file-in-django
def _update_filename(instance, filename, path):
    return os.path.join(path, filename)

def upload_to(path):
    return partial(_update_filename, path=path)

class S3Upload(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)

class S3NavUpload(S3Upload):
    file = models.FileField(upload_to=('site_pages/site_look/nav_image'))

class S3FaviconUpload(S3Upload):
    file = models.FileField(upload_to=('images'))

class S3HomeBackgroundUpload(S3Upload):
    file = models.FileField(upload_to=('site_pages/home/bg_image'))

class S3TopicsHeaderUpload(S3Upload):
    file = models.FileField(upload_to='site_pages/topics/header_image')

class S3AboutHeaderUpload(S3Upload):
    file = models.FileField(upload_to='site_pages/about/header_image')

class S3ContactHeaderUpload(S3Upload):
    file = models.FileField(upload_to=('site_pages/contact/header_image'))

class S3ContribHeaderUpload(S3Upload):
    file = models.FileField(upload_to=('site_pages/contrib/header_image'))

class S3AboutBox1Upload(S3Upload):
    file = models.FileField(upload_to='site_pages/about/box1_image')

class S3AboutBox2Upload(S3Upload):
    file = models.FileField(upload_to='site_pages/about/box2_image')

class S3PostsUpload(S3Upload):
    file = models.FileField(upload_to='site_pages/posts/images')

class S3TopicsUpload(S3Upload):
    file = models.FileField(upload_to='site_pages/topics/topic_splash_images')

class S3AuthorProfileUpload(S3Upload):
    file = models.FileField(upload_to='site_pages/authors/profile_images')

class S3SubscribeFormBoxImgUpload(S3Upload):
    file = models.FileField(upload_to='site_pages/forms/subscriber_form/box_img')

class FormSendFailure(models.Model):
    """Class used to log failures in emailing submitted form data so that
    the data is preserved.
    """
    to        = models.EmailField()
    form_name = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    exception = models.CharField(max_length=500)
    form_data = models.TextField(max_length=600) # Parse as string and use eval() to convert back to dict
    resent_ok = models.BooleanField(default=False)


class NewsletterSendFailure(models.Model):
    to            = models.EmailField()
    template_used = models.CharField(max_length=20)
    template_id   = models.IntegerField()
    timestamp     = models.DateTimeField(auto_now_add=True)
    exception     = models.CharField(max_length=500)
    resent_ok     = models.BooleanField(default=False)


class SiteLook(models.Model):
    """Contains attributes that determine the content of the nav and footer."""
    show_home      = models.BooleanField(default=False)
    show_topics    = models.BooleanField(default=True)
    show_timeline  = models.BooleanField(default=True)
    show_contact   = models.BooleanField(default=True)
    show_contrib   = models.BooleanField(default=True)
    show_about     = models.BooleanField(default=True)

    footer_copyright     = models.CharField(max_length=100)
    footer_tagline       = models.CharField(max_length=40)
    footer_about         = models.CharField(max_length=300)
    footer_location      = models.CharField(max_length=800)
    footer_contact_phone = models.CharField(max_length=21)
    footer_contact_email = models.CharField(max_length=320)

    font    = models.TextField()
    favicon = models.FileField()

    navigation_img      = models.FileField()
    navigation_img_size = models.CharField(max_length=12, blank=True, null=True)

    footer_text_color = models.CharField(max_length=10)
    footer_color      = ColorField(default='#43897F')

    lat = models.CharField(max_length=200)
    lon = models.CharField(max_length=200)


class Home(models.Model):
    """Contains attributes that determine the content of the home page."""
    alert_banner   = models.CharField(max_length=900, blank=True, null=True)
    tagline        = models.TextField(max_length=200, blank=True, null=True)
    tagline_size   = models.CharField(max_length=2) # Use h1, h2, or h3 as options.
    tagline_color  = ColorField(default='#FFFFFF')
    tagline_shadow = models.BooleanField(default=False)
    email_addr     = models.CharField(max_length=320, blank=True, null=True)
    # Max lengths determined by https:// scheme +
    # host_name/ + filepath (if any) + max length of username.
    facebook_link  = models.CharField(max_length=75, blank=True, null=True)
    github_link    = models.CharField(max_length=58, blank=True, null=True)
    instagram_link = models.CharField(max_length=56, blank=True, null=True)
    twitter_link   = models.CharField(max_length=35, blank=True, null=True)
    youtube_link   = models.CharField(max_length=49, blank=True, null=True)

    # These lengths are arbitrary
    about_label    = models.CharField(max_length=200, blank=True, null=True)
    donate_label   = models.CharField(max_length=200, blank=True, null=True)

    background_img = models.FileField()


class Topics(models.Model):
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField(null=True, blank=True)
    header_image_file_name = models.TextField()
    header_text            = models.CharField(max_length=75)


class About(models.Model):
    """Contains attributes that determine the content of the about page."""
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField(null=True, blank=True)
    header_image_file_name = models.TextField()
    header_text            = models.CharField(max_length=75)

    box1_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box1_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box1_img           = models.FileField()
    box1_img_alt       = models.CharField(max_length=75)
    box1_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box1_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box1_img_file_name = models.TextField()

    box2_header_text   = models.CharField(max_length=75, blank=True, null=True)
    box2_content_text  = models.CharField(max_length=6000, blank=True, null=True)
    box2_img           = models.FileField()
    box2_img_alt       = models.CharField(max_length=75)
    box2_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box2_img_position  = models.CharField(max_length=22, blank=True, null=True)
    box2_img_file_name = models.TextField()


class Contact(models.Model):
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField(null=True, blank=True)
    header_image_file_name = models.TextField()
    header_text            = models.CharField(max_length=75)

    phone_fax_header_text = models.CharField(max_length=75, blank=True, null=True)
    contact_phone         = models.CharField(max_length=21, blank=True, null=True)
    contact_fax           = models.CharField(max_length=21, blank=True, null=True)

    addr_mail_header_text = models.CharField(max_length=75, blank=True, null=True)
    contact_address       = models.CharField(max_length=900, blank=True, null=True)
    contact_mailbox       = models.CharField(max_length=900, blank=True, null=True)

    contact_email_addr = models.CharField(max_length=320, blank=True, null=True)

    show_contact_form    = models.BooleanField(default=True)

    contact_form_message = models.CharField(
        max_length=150,
        default=(
            "Want to get in touch or leave feedback?" \
            " Leave a short message below."
        )
    )

    contact_mail_template_id = models.IntegerField(default=0)


class Contrib(models.Model):
    show_header_image      = models.BooleanField(default=True)
    header_image           = models.FileField(null=True, blank=True)
    header_image_file_name = models.TextField()
    header_text            = models.CharField(max_length=75)
    contrib_form_message   = models.CharField(
        max_length=150,
        default=(
            "Interested in contributing to this blog?" \
            " Enter your information below and I will contact you via your email address."
        )
    )
    contrib_mail_template_id = models.IntegerField(default=0)


class Topic(models.Model):
    name = models.CharField(max_length=250)
    is_featured          = models.BooleanField(default=False)
    splash_img           = models.FileField()
    splash_img_file_name = models.TextField()


class AuthorProfile(models.Model):
    preferred_name = models.CharField(max_length=100)
    profile_icon   = models.FileField(null=True, blank=True)
    profile_icon_file_name = models.TextField()
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bio  = models.CharField(max_length=1000)


class Post(models.Model):
    """Represents an individual blog post."""
    title    = models.CharField(max_length=200)
    slug     = models.SlugField(null=True, blank=True, max_length=200)
    date     = models.DateField(auto_now=True)
    og_date  = models.DateField(auto_now_add=True)
    location = models.CharField(max_length=250)
    author   = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)
    topics   = models.ManyToManyField(Topic)

    # M-M documentation: https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
    is_featured       = models.BooleanField(default=False)
    visibility        = models.CharField(max_length=8)
    box_content_text  = models.TextField(blank=True, null=True)
    box_img           = models.FileField()
    box_img_credit    = models.CharField(max_length=300)
    box_img_alt       = models.CharField(max_length=75)
    box_img_size      = models.CharField(max_length=12, blank=True, null=True)
    box_img_file_name = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.title)

        super(Post, self).save(*args, **kwargs)


class PostCollaborator(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(AuthorProfile, on_delete=models.CASCADE)    


class Thread(models.Model):
    og_date  = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    post_id = models.IntegerField()
    og_date = models.DateTimeField(auto_now_add=True)
    name    = models.CharField(max_length=200)
    text    = models.CharField(max_length=500)
    orig    = models.BooleanField(default=False)
    thread  = models.ForeignKey(Thread, on_delete=models.CASCADE)


class SEO(models.Model):
    """Contains attributes that determine meta information for SEO."""
    meta_title       = models.CharField(max_length=100)
    meta_description = models.CharField(max_length=190)
    meta_keywords    = models.CharField(max_length=3000)
    meta_author      = models.CharField(max_length=100)

    robots_index  = models.BooleanField(
        default=True,
        help_text='See https://moz.com/learn/seo/robots-meta-directives'
    )

    robots_follow = models.BooleanField(
        default=True,
        help_text='See https://moz.com/learn/seo/robots-meta-directives'
    )

    robots_index_str  = models.CharField(max_length=7, default='index')
    robots_follow_str = models.CharField(max_length=8, default='follow')

    google_analytics_script = models.CharField(max_length=2200, default='')
    hotjar_script           = models.CharField(max_length=2200, default='')

    def save(self, *args, **kwargs):
        if self.robots_index:
            self.robots_index_str = 'index'
        else:
            self.robots_index_str ='noindex'
        
        if self.robots_follow:
            self.robots_follow_str = 'follow'
        else:
            self.robots_follow_str = 'nofollow'
        
        super(SEO, self).save(*args, **kwargs)
        


class EmailAccount(models.Model):
    """Contains the email address for which form data should be sent to."""
    email_addr = models.CharField(max_length=320, blank=False, null=False)


class DenylistEmail(models.Model):
    """Contains attributes to represent an email address for which no forms submitted with this address should be emailed."""
    email_addr = models.CharField(max_length=320, blank=False, null=False)
    comment    = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'denylistemails'


class SubscriberNewsletter(models.Model):
    """This model determines the caharacteristics of the newsletter that gets send out to subscribers"""
    send_interval  = models.CharField(max_length=5, blank=False, null=False, default='month', choices=NewsletterOptions.SEND_INTERVALS)
    week_send_day  = models.PositiveSmallIntegerField(max_length=1, default=0, choices=NewsletterOptions.WEEK_SEND_DAYS) # 0 == Monday
    send_hour      = models.PositiveSmallIntegerField(default=12, choices=NewsletterOptions.SEND_HOURS)
    send_minute    = models.PositiveSmallIntegerField(default=0, choices=NewsletterOptions.SEND_MINS)
    custom_message = models.CharField(max_length=500)

    num_featured_posts = models.PositiveSmallIntegerField(default=3, choices=NewsletterOptions.NUM_FEATURED_POSTS)
    num_recent_posts   = models.PositiveSmallIntegerField(default=0, choices=NewsletterOptions.NUM_RECENT_POSTS)

    featured_template_id = models.IntegerField(default=0)
    recent_template_id   = models.IntegerField(default=0)
    both_template_id     = models.IntegerField(default=0)
    site_url             = models.CharField(max_length=200, default='')
    unsubscribe_url      = models.CharField(max_length=218, default='')


class EmailContactFormSettings(models.Model):
    show_form = models.BooleanField(default=False)
    message   = models.CharField(max_length=50,
                    default='Interested in learning more? Leave me your email.')
    mail_template_id = models.IntegerField(default=0)


class SubscribeFormSettings(models.Model):
    """Unlike SubscriberNewsletter, this model determines how the form appears to users."""
    show_form         = models.BooleanField(default=False)
    title             = models.CharField(max_length=28, default='Subscribe to my newsletter')
    message           = models.CharField(max_length=150)
    box_img           = models.FileField()
    box_img_credit    = models.CharField(max_length=300)
    box_img_alt       = models.CharField(max_length=75)
    box_img_file_name = models.TextField()
    subscribed_mail_template_id = models.IntegerField(default=0)