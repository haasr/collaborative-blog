from admin_pages.models import *
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from blog import settings
import os

DEFAULT_FONT = """<link href="https://fonts.googleapis.com/css2?family=Barlow:wght@500&display=swap" rel="stylesheet">&&Barlow"""

x = SiteLook(
    id=1,
    show_home=True,
    show_topics=True,
    show_contrib=True,
    show_contact=True,
    show_about=True,
    font=DEFAULT_FONT,
    footer_tagline="My cool blog",
    footer_copyright="Cool Person, 2022",
    footer_about="Welcome to my cool blog!",
    footer_text_color='text-light',
    navigation_img_size='width: 30%;',
)
x.save()

x = Home(
    id=1, 
    alert_banner='',
    tagline="\"We are just temporary bubbles in the foamy head of the universe's beer.\" - G",
    tagline_shadow=True,
    tagline_size='h2',
    tagline_color='#FFFFFF',
    email_addr='',
    facebook_link='',
    github_link='',
    instagram_link='',
    twitter_link='',
    youtube_link='',
    about_label='About Me',
    donate_label='',
)
x.save()

x = Topics(
    id=1,
    show_header_image=True,
    header_image_file_name='topics-header.jpg',
    header_text='',
)
x.save()

x = Topic( # An error will occur if at least one topic does not exist
    id=1,
    name='NEWS',
)
x.save()

x = Contrib(
    id=1,
    show_header_image=True,
    header_image_file_name='',
    header_text='Contribute',
)
x.save()

x = About(
    id=1,
    show_header_image=True,
    header_image_file_name='about-header.jpg',
    header_text='',
    box1_header_text='',
    box1_content_text='',
    box1_img_file_name='',
    box2_header_text='',
    box2_content_text='',
    box2_img_file_name='',
)
x.save()

x = Contact(
    id=1,
    show_header_image=True,
    header_text='',
    header_image_file_name='contact-header.png',
    phone_fax_header_text='Phone & Fax',
    contact_phone='123.456.7891',
    contact_fax='123.456.7892',
    addr_mail_header_text='Address & Mail',
    contact_address='123 Mulberry Ln City, ST 12345',
    contact_mailbox='P.O. Box 1',
    contact_email_addr='contact@email.com',
    contact_mail_template_id=0
)
x.save()

x = Contrib(
    id=1,
    show_header_image=True,
    header_text='',
    header_image_file_name='contrib-header.jpg',
    contrib_mail_template_id=0
)
x.save()

x = EmailContactFormSettings(
    id=1,
    mail_template_id=0
)
x.save()

x = SubscribeFormSettings(
    id=1,
    message='',
    box_img_credit='',
    box_img_alt='',
    box_img_file_name=''
)
x.save()

x = SEO(
    id=1,
    meta_title='',
    meta_description='',
    meta_keywords='',
    meta_author='',
    robots_index=True,
    robots_follow=True,
)
x.save()

x = EmailAccount(
    id=1,
    email_addr='',
)
x.save()

x = SubscriberNewsletter(
    id=1,
    custom_message="Check out this month's featured posts.",
)
x.save()

print('WARNING')
print('In the following prompts, I was too lazy to add input validation, so take your time :)')
print('If you mess up, just break out with Ctrl-C and restart the script.')
input('Enter to continue...')

print('\n###### Create initial admin account ######')
print('You must create an initial admin account\nto log into <hostname>/accounts/login/\n')
fname  = input('  First Name: ')
lname  = input('  Last Name:  ')
mail   = input('  Email:      ')
uname  = input('  Username:   ')
pswd   = input('  Password:   ')

new_usr = User.objects.create_user(first_name=fname, last_name=lname, email=mail,
                                    username=uname, password=pswd, is_staff=True)
new_usr.save()
new_usr.is_staff = True
new_usr.is_superuser = True
new_usr.save()

a = AuthorProfile(
    preferred_name=( fname + ' ' + lname ),
    user=new_usr
)
a.save()


# This is to prevent authenticator app from listing site as example.com:

print('\n###### Specify site name & domain ######')
site_name = input("  Your site's name: ")
domain    = input("  Your domain (e.g., yourblog.com, don't need https:// or wwww prefix): ")

site = Site(id=1, domain=domain, name=site_name)
site.save()

# And might as well populate this for them:
seo = SEO.objects.get(id=1)
seo.meta_title = site_name
seo.save()