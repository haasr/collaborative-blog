from django import forms
from admin_pages import models_options

from .models import *
from colorfield.fields import ColorField
from crispy_forms.helper import FormHelper

from .forms_options import *
from .models_options import NewsletterOptions

class SiteLookForm(forms.ModelForm):
    show_home = forms.BooleanField(
        label='Shome Home Page in Nav',
        required=False,
    )

    show_topics = forms.BooleanField(
        label='Show Topics Page',
        required=False,
    )

    show_timeline = forms.BooleanField(
        label='Show Timeline Page',
        required=False
    )

    show_contact = forms.BooleanField(
        label='Show Contact Page',
        required=False,
    )

    show_contrib = forms.BooleanField(
        label='Show Contrib Page',
        required=False,
    )

    show_about = forms.BooleanField(
        label='Show About Page',
        required=False,
    )

    footer_copyright = forms.CharField(
        label='Footer copyright text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., 2022 - Ryan Haas, All rights reserved.'
        })
    )

    footer_tagline = forms.CharField(
        label='Short tagline (40 char. max)',
        required=False,
    )

    footer_about = forms.CharField(
        label='About Statement',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '3',
            'cols': '40',
            'placeholder': 'Enter a short about statement'
        })
    )

    footer_location = forms.CharField(
        label='Enter street address',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., 123 Mulberry Ln City, ST 12345'
        })
    )

    lat = forms.CharField(
        label='Map Address latitude',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., 35.956332'
        })
    )

    lon = forms.CharField(
        label='Map Address longitude',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., -83.923854'
        })
    )

    footer_contact_phone = forms.CharField(
        label='Contact Phone Number',
        required=False,
    )

    footer_contact_email = forms.EmailField(
        label='Contact Email Address',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ContactEmail@example.com'
        })
    )

    footer_text_color = forms.CharField(
        label='Text Color for footer',
        required=True,
        widget=forms.Select(
            choices=TextOptions.TEXT_COLORS
        )
    )

    navigation_img = forms.FileField(
        label='Nav Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    navigation_img_size = forms.CharField(
        label='Nav Image Size',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    favicon = forms.FileField(
        label='Favicon Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/x-icon'
        })
    )

    font = forms.CharField(
        label='Font',
        required=False,
        widget=forms.Select(
            choices=FontOptions.GOOGLE_FONTS
        )
    )

    font_preview = forms.CharField(
        label='Font Preview',
        required=False,
    )

    footer_color = ColorField()

    class Meta:
        model = SiteLook
        fields = [
            'show_home', 'show_topics', 'show_timeline', 'show_contact',
            'show_contrib', 'show_about', 'navigation_img', 'navigation_img_size',
            'favicon', 'font', 'font_preview', 'footer_text_color', 'footer_color',
            'footer_copyright', 'footer_tagline', 'footer_about',
            'footer_contact_phone', 'footer_contact_email', 'footer_location',
            'lat', 'lon'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class HomeForm(forms.ModelForm):
    background_img = forms.FileField(
        label='Splash Image (2000x900px recommended):',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )
    
    alert_banner = forms.CharField(
        label='Alert Banner',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': 'Enter an alert to display atop the page.'
        })
    )

    tagline = forms.CharField(
        label='Tagline',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': 'Enter a short tagline here.'
        })
    )

    tagline_size = forms.CharField(
        label='Tagline size',
        required=True,
        widget=forms.Select(
            choices=TextOptions.HEADER_SIZES
        )
    )

    tagline_shadow = forms.BooleanField(
        label='Tagline shadow',
        required=False,
    )

    tagline_color = ColorField()

    # In the view, make this a link by prepending the
    # mailto in front.
    email_addr = forms.EmailField(
        label='Contact Email',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ContactEmail@example.com'
        })
    )

    facebook_link = forms.URLField(
        label='Facebook Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.facebook.com/yourUsername'
        })
    )

    github_link = forms.URLField(
        label='Github Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://github.com/yourUsername'
        })
    )

    twitter_link = forms.URLField(
        label='Twitter Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.twitter.com/yourUsername'
        })
    )

    instagram_link = forms.URLField(
        label='Instagram Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.instagram.com/yourUsername'
        })
    )

    youtube_link = forms.URLField(
        label='YouTube Profile',
        required=False,
        widget=forms.URLInput(attrs={
            'placeholder': 'https://www.youtube.com/user/yourChannelName'
        })
    )

    about_label = forms.CharField(
        label='About Link Label',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., About Me'
        })
    )

    donate_label = forms.CharField(
        label='Donate Link Label',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Donate'
        })
    )

    class Meta:
        model = Home
        fields = [
            'background_img', 'alert_banner', 'tagline', 'tagline_size', 
            'tagline_shadow', 'tagline_color', 'email_addr', 'facebook_link',
            'github_link', 'instagram_link', 'twitter_link', 'youtube_link',
            'about_label', 'donate_label'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class TopicsPageForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Main Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Browse site topics'
        })
    )
    class Meta:
        model = Topics
        fields = [
            'show_header_image', 'header_image', 'header_text'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class AboutForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Main Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Get to know me'
        })
    )

    box1_header_text = forms.CharField(
        label='Box 1 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., My Story'
        })
    )

    box1_img = forms.FileField(
        label='Box 1 Image:',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box1_img_alt = forms.CharField(
        label='Box 1 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box1_img_size = forms.CharField(
        label='Box 1 Image Size',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box1_img_position = forms.CharField(
        label='Box 1 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    box1_content_text = forms.CharField(
        label='Box 1 Content Text',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 1\'s content here.')
        })
    )

    box2_header_text = forms.CharField(
        label='Box 2 Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., About this site'
        })
    )

    box2_img = forms.FileField(
        label='Box 2 Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box2_img_alt = forms.CharField(
        label='Box 2 Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box2_img_size = forms.CharField(
        label='Box 2 Image Size',
        required=False,
        widget=forms.Select(
            choices=ImageOptions.PERCENTAGES
        )
    )

    box2_img_position = forms.CharField(
        label='Box 2 Image Position',
        required=False,
        widget = forms.Select(
            choices=ImageOptions.POSITIONS
        )
    )

    box2_content_text = forms.CharField(
        label='Box 2 Content Text',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '10',
            'cols': '40',
            'placeholder': ('Enter Box 2\'s content here.')
        })
    )

    class Meta:
        model = About
        fields = [ 
            'show_header_image', 'header_image', 'header_text',
            'box1_header_text', 'box1_content_text', 'box1_img', 'box1_img_alt',
            'box1_img_size', 'box1_img_position','box2_header_text', 'box2_content_text',
            'box2_img', 'box2_img_alt', 'box2_img_size', 'box2_img_position',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class ContactForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Get in touch.'
        })
    )

    phone_fax_header_text = forms.CharField(
        label='Phone & Fax Header',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Phone and Fax'
        })
    )

    contact_phone = forms.CharField(
        label='Contact Phone Number',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tip: Don\'t include spaces'
        })
    )

    contact_fax = forms.CharField(
        label='Contact Fax Number',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Tip: Don\'t include spaces'
        })
    )


    addr_mail_header_text = forms.CharField(
        label='Address & Mail Header',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Address and Mail'
        })
    )

    contact_address = forms.CharField(
        label='Church Address',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., 123 Mulberry Ln City, ST 12345'
        })
    )

    contact_mailbox = forms.CharField(
        label='Mail/P.O. Box',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., P.O. Box 8'
        })
    )

    contact_email_addr = forms.EmailField(
        label='Contact Email Address',
        required=False,
        widget=forms.EmailInput(attrs={
            'placeholder': 'ContactEmail@example.com'
        })
    )

    show_contact_form = forms.BooleanField(
        label='Show Contact Form',
        required=False,
    )

    class Meta:
        model = Contact
        fields = [
            'show_header_image', 'header_image', 'header_text',
            'phone_fax_header_text', 'contact_phone', 'contact_fax',
            'addr_mail_header_text', 'contact_address', 'contact_mailbox',
            'contact_email_addr', 'show_contact_form'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class ContribForm(forms.ModelForm):
    show_header_image = forms.BooleanField(
        label='Show Header Image',
        required=False,
    )

    header_image = forms.FileField(
        label='Header Image (~3200x1500px recommended)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    header_text = forms.CharField(
        label='Header Text',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Contribute content to this blog.'
        })
    )

    class Meta:
        model = Contrib
        fields = [
            'show_header_image', 'header_image', 'header_text',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class AddTopicForm(forms.ModelForm):
    topic_choice = forms.CharField(
        label='Pre-existing Topics',
        widget=forms.Select(
            choices=[ (t, t) for t in Topic.objects.all()._clone().values_list('name', flat=True) ]
        )
    )
    
    name = forms.CharField(
        label='Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Art, Science, Pop Culture'
        })
    )

    class Meta:
        model = Topic
        fields = [ 'topic_choice', 'name' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class TopicForm(forms.ModelForm):
    name = forms.CharField(
        label='Name',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Art, Science, Pop Culture'
        })
    )

    is_featured = forms.BooleanField(
        label='Is featured',
        required=False,
    )

    splash_img = forms.FileField(
        label = 'Splash Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    def clean_name(self):
        return self.cleaned_data['name'].upper()

    class Meta:
        model = Topic
        fields = [ 
            'name', 'is_featured', 'splash_img',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class PostCollabForm(forms.Form):
    collab_choices = forms.MultipleChoiceField(
        label='Add or remove collaborators',
        widget=forms.CheckboxSelectMultiple,
        required=False,
        choices=([ a_tuple for a_tuple in AuthorProfile.objects.all() \
                .values_list('id', 'preferred_name') ])
    )

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostCollabForm, self).__init__(*args, **kwargs)

        # Discluding author passed (current author for auth'd acc't):
        choices = self.fields['collab_choices'].choices
        idx = choices.index((self.author.id, self.author.preferred_name))
        choices.pop(idx) # Byeeeee

        self.helper = FormHelper()
        self.helper.label_class='fs-450'
        self.helper.form_tag = False


class PostForm(forms.ModelForm):
    title = forms.CharField(
        label='Title',
        required=True,
    )

    location = forms.CharField(
        label='Location',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Place, City, ST'
        })
    )

    is_featured = forms.BooleanField(
        label='Is featured',
        required=False,
    )

    visibility = forms.CharField(
        label='Post Visibility',
        required=True,
        widget=forms.Select(
            choices=PostOptions.VISIBILITY
        )
    )

    box_img = forms.FileField(
        label='Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box_img_credit = forms.CharField(
        label='Image Credit',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Credit source',
        })
    )

    box_img_alt = forms.CharField(
        label='Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    box_content_text = forms.CharField(
        label='Article Body',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '20',
            'cols': '30',
        })
    )

    class Meta:
        model = Post
        fields = [
            'title', 'location', 'is_featured', 'visibility', 'box_img',
            'box_img_credit', 'box_img_alt', 'box_content_text',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class CommentForm(forms.ModelForm):
    name = forms.CharField(
        label='Display Name',
        required=False
    )

    text = forms.CharField(
        label='Comment',
        required=False,
        max_length=500,
        widget=forms.Textarea(attrs={
            'rows': '8',
            'cols': '40',
            'placeholder': 'Limit: 500 characters'
        })
    )

    class Meta:
        model = Comment
        fields = [ 'name', 'text' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class PostImageForm(forms.ModelForm):
    box_img = forms.FileField(
        label='Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box_img_credit = forms.CharField(
        label='Image Credit',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Credit source',
        })
    )

    box_img_alt = forms.CharField(
        label='Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    class Meta:
        model = Post
        fields = [
            'box_img', 'box_img_credit', 'box_img_alt',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class AuthorProfileForm(forms.ModelForm):
    profile_icon = forms.FileField(
        label='Profile image (1:1 Aspect Ratio)',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    preferred_name = forms.CharField(
        label='Preferred/Display Name',
        required=True
    )

    bio = forms.CharField(
        label='Bio',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': 'Tell readers about yourself in 500 characters or less.'
        }) 
    )

    class Meta:
        model = AuthorProfile
        fields = [
            'profile_icon', 'preferred_name', 'bio'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class SEOForm(forms.ModelForm):
    meta_title = forms.CharField(
        label='Site Title',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Ryan\'s Reflections'
        })
    )

    meta_description = forms.CharField(
        label='Site Description',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
        })
    )

    meta_keywords = forms.CharField(
        label='Site Keywords',
        required=True,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': ('Help search engines identify the site.\n'
                            'Ex. keywords: blog, philosophy, music'),
        })
    )

    meta_author = forms.CharField(
        label='Site Author',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'E.g., Ryan Haas'
        })
    )

    robots_index = forms.BooleanField(
        label='Let bots index pages',
        required=False,
    )

    robots_follow = forms.BooleanField(
        label='Let bots crawl links',
        required=False,
    )

    class Meta:
        model = SEO
        fields = [
            'meta_title', 'meta_description', 'meta_keywords', 'meta_author',
            'robots_index', 'robots_follow'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class EmailAccountForm(forms.ModelForm):
    email_addr = forms.EmailField(
        label='Email Recipient',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'SiteEmail@example.com'
        })
    )

    class Meta:
        model = EmailAccount
        fields = [ 'email_addr', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class DenylistEmailForm(forms.ModelForm):
    email_addr = forms.EmailField(
        label='Email Address',
        required=True,
    )

    comment = forms.CharField(
        label='Comment',
        required=False,
    )

    class Meta:
        model = DenylistEmail
        fields = [ 'email_addr', 'comment' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class ViewerContactFormSettingsForm(forms.ModelForm):
    show_contact_form = forms.BooleanField(
        label='Show Form',
        required=False,
    )

    contact_form_message = forms.CharField(
        label='Form message',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': (
                'Custom message below form title. 150 characters or less.'
            )
        })
    )

    contact_mail_template_id = forms.IntegerField(
        label='Email Template ID',
        help_text="The email template ID to send the contact info to your configured email inbox."
    )

    class Meta:
        model = Contact
        fields = [
            'show_contact_form', 'contact_form_message', 'contact_mail_template_id'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class EmailContactFormSettingsForm(forms.ModelForm):
    show_form = forms.BooleanField(
        label='Show Form',
        required=False,
    )

    message = forms.CharField(
        label='Form Message',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': (
                'Custom message above form. 50 characters or less.'
            )
        })
    )

    mail_template_id = forms.IntegerField(
        label='Email Template ID',
        help_text="The email template ID to send the contact info to your configured email inbox."
    )

    class Meta:
        model = EmailContactFormSettings
        fields = [ 'show_form', 'message', 'mail_template_id' ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class ContributeFormSettingsForm(forms.ModelForm):
    contrib_form_message = forms.CharField(
        label='Form message',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': (
                'Custom message below form title. 150 characters or less.'
            )
        })
    )

    contrib_mail_template_id = forms.IntegerField(
        label='Email Template ID',
        help_text="The email template ID to send the contribute info to your configured email inbox."
    )

    class Meta:
        model = Contrib
        fields = [
            'contrib_form_message', 'contrib_mail_template_id'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class SubscribeFormSettingsForm(forms.ModelForm):
    show_form = forms.BooleanField(
        label='Show Form / Enable Newsletter',
        required=False,
    )

    title = forms.CharField(
        label='Title',
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder': 'e.g., Subscribe'
        })
    )

    message = forms.CharField(
        label='Message',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '2',
            'cols': '40',
            'placeholder': (
                'Custom message below form title. 150 characters or less.'
            )
        })
    )

    box_img = forms.FileField(
        label='Image',
        required=False,
        widget=forms.FileInput(attrs={
            'multiple': False,
            'accept': 'image/*'
        })
    )

    box_img_credit = forms.CharField(
        label='Image Credit',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Credit source',
        })
    )

    box_img_alt = forms.CharField(
        label='Image Alt',
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Describe the image'
        })
    )

    subscribed_mail_template_id = forms.IntegerField(
        label='Subscribed Mail Template ID',
        help_text="The email template ID to send a 'subscribed' confirmation email."
    )

    class Meta:
        model = SubscribeFormSettings
        fields = [
            'show_form', 'title', 'message', 'box_img',
            'box_img_credit', 'box_img_alt', 'subscribed_mail_template_id'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class SubscriberNewsletterForm(forms.ModelForm):
    send_interval = forms.CharField(
        label='Send Interval',
        widget=forms.Select(
            choices=NewsletterOptions.SEND_INTERVALS
        )
    )

    week_send_day = forms.ChoiceField(
        label='Send Day',
        choices=NewsletterOptions.WEEK_SEND_DAYS,
        help_text='When Send Interval is \"Each month\", it will send on the first' \
          ' matching day of the month (e.g., first Mon, Tue, etc.)'
    )

    send_hour = forms.ChoiceField(
        label='Hour to send',
        choices=NewsletterOptions.SEND_HOURS
    )

    send_minute = forms.ChoiceField(
        label='Minute to send',
        choices=NewsletterOptions.SEND_MINS
    )

    num_featured_posts = forms.ChoiceField(
        label='Number of featured posts',
        choices=NewsletterOptions.NUM_FEATURED_POSTS,
        help_text='Show up to 3 featured posts in the newsletter'
    )

    num_recent_posts = forms.ChoiceField(
        label='Number of recent posts',
        choices=NewsletterOptions.NUM_RECENT_POSTS,
        help_text='Show up to 3 recent posts in the newsletter'
    )

    featured_template_id = forms.IntegerField(
        label='Featured Posts Template ID',
        help_text="The email template ID to send a 'Featured Posts' newsletter."
    )

    recent_template_id = forms.IntegerField(
        label='Recent Posts Template ID',
        help_text="The email template ID to send a 'Recent Posts' newsletter."
    )

    both_template_id = forms.IntegerField(
        label='Template ID for Featured + Recent Posts',
        help_text="The email template ID to send a 'Featured & Recent Posts' newsletter."
    )

    site_url = forms.CharField(
        label="Your site's home URL",
        widget=forms.URLInput(attrs={
            'placeholder': 'E.g., https://yourblog.com/'
        })
    )

    def clean_custom_message(self):
        return (self.cleaned_data['custom_message'][0].lower()
                    + self.cleaned_data['custom_message'][1:])

    class Meta:
        model = SubscriberNewsletter
        fields = [
            'send_interval', 'week_send_day',
            'send_hour', 'send_minute', 'custom_message',
            'num_featured_posts', 'num_recent_posts',
            'featured_template_id', 'recent_template_id',
            'both_template_id', 'site_url'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False
