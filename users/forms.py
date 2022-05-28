from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import SetPasswordForm
from crispy_forms.helper import FormHelper
from password_validator import PasswordValidator


schema1 = PasswordValidator()
schema2 = PasswordValidator()

schema1\
.min(8)\
.max(50)\
.has().uppercase()\
.has().lowercase()\

schema2\
.has().digits()\
.has().no().spaces()



class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username',
        required=True,
    )

    password = forms.CharField(
        label='Password',
        required=True,
        widget=forms.PasswordInput()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class SignUpForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=30, required=True)
    email      = forms.EmailField(max_length=254, required=True)
    username   = forms.CharField(max_length=30, required=True)

    password   = forms.CharField(max_length=30, required=True,
        widget=forms.PasswordInput()
    )

    is_superuser = forms.BooleanField(
        label='Admin Priveleges',
        required=False,
    )

    def clean_username(self):
        if User.objects.filter(username=self.cleaned_data['username'].lower()).exists():
            self.add_error('username', 'An account with this username already exists.')
        return self.cleaned_data['username']

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email'].lower()).exists():
            self.add_error('email', 'An account with this email address already exists.')
        return self.cleaned_data['email']

    def clean_password(self):
        passwd = self.cleaned_data['password']

        # Check password requirements
        if len(passwd) < 9:
            self.add_error('password', "Password must be 9-50 characters")
        if not schema1.validate(passwd):
            self.add_error('password', "Password must have an uppercase and a lowercase letter")
        if not schema2.validate(passwd):
            self.add_error('password', "Password must contain a digit and no spaces")

        return passwd

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'is_superuser' )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class UpdateUserForm(forms.Form):
    first_name = forms.CharField(max_length=30, required=True)
    last_name  = forms.CharField(max_length=30, required=True)
    email      = forms.EmailField(max_length=254, required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False


class CustomSetPasswordForm(SetPasswordForm):
    def clean_new_password2(self):
        passwd1 = self.cleaned_data['new_password1']
        passwd2 = self.cleaned_data['new_password2']

        if passwd1 and passwd2:
            # Check that passwords match
            if passwd1 != passwd2:
                self.add_error('new_password2', 'The passwords do not match.')

            # Check password requirements
            if len(passwd1) < 9:
                self.add_error('new_password1', "Password must be 9-50 characters")
            if not schema1.validate(passwd1):
                self.add_error('new_password1', "Password must have an uppercase and a lowercase letter")
            if not schema2.validate(passwd1):
                self.add_error('new_password1', "Password must contain a digit and no spaces")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class='form-horizontal'
        self.helper.label_class='col-25 fs-400 ff-sans-normal'
        self.helper.field_class='col-75'
        self.helper.form_tag = False