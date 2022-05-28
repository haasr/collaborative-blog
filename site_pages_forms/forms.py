from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column

class EmailSubscriberForm(forms.Form):
    subscriber_fname = forms.CharField(
        label='First Name',
        required=True
    )

    subscriber_lname = forms.CharField(
        label='Last Name',
        required=False
    )

    subscriber_email = forms.CharField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'yourEmail@example.com'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class EmailContactForm(forms.Form):
    viewer_email = forms.EmailField(
        label=False,
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your email address'
        })
    )


class ViewerContactForm(forms.Form):
    fname = forms.CharField(
        label='First Name',
        required=True
    )

    lname = forms.CharField(
        label='Last Name',
        required=False
    )

    email = forms.EmailField(
        label='Your Email Address',
        required=True
    )

    comment = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class ContributeForm(forms.Form):
    fname = forms.CharField(
        label='First Name',
        required=True,
    )

    lname = forms.CharField(
        label='Last Name',
        required=True,
    )

    email = forms.EmailField(
        label='Email Address',
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Your contact email address'
        })
    )

    uname = forms.CharField(
        label='Desired username',
        required=True,
    )

    about = forms.CharField(
        label='Comment',
        required=False,
        widget=forms.Textarea(attrs={
            'rows': '4',
            'cols': '40',
            'placeholder': (
                'Introduce yourself. How would you like to contribute?'
            )
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400'
        self.helper.field_class='col-75'
        self.helper.form_tag = False