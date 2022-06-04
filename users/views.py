from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django_otp.decorators import otp_required
from custom_decorators.decorators import is_superuser
from admin_pages.models import AuthorProfile
from .forms import *


def login_view(request):
    logout(request)
    if request.method != 'POST':
        form = LoginForm()
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])

            if not (user is None):
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('admin_pages:admin_index'))
            else:
                messages.error(request, 'Username or password not correct')
                return redirect('users:login')

    context = { 'form': form }
    return render(request, 'users/login.html', context)


def logout_view(request):
    """Log the user out."""
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@is_superuser
@otp_required
def register(request):
    """Register a new user."""
    if (request.method != 'POST'):
        form = SignUpForm()
    else:
        form = SignUpForm(data=request.POST)

        if (form.is_valid()):
            data = form.cleaned_data
            new_usr = User.objects.create_user(username=data['username'], email=data['email'],
                                                password=data['password'])
            new_usr.save()

            fname = data['first_name']
            lname = data['last_name']
            new_usr.first_name = fname
            new_usr.last_name = lname
            new_usr.is_staff = True
            new_usr.is_superuser = data['is_superuser']

            new_usr.save()
            new_usr.refresh_from_db()

            a = AuthorProfile(
                preferred_name=(fname + ' ' + lname),
                user=new_usr
            )
            a.save()

            return HttpResponseRedirect(reverse('admin_pages:manage_users'))

    context = { 'form': form }
    return render(request, 'users/register.html', context)


@otp_required
def update_user(request, posts_redirect):
    user = User.objects.get(id=request.user.id)

    if request.method != 'POST':
        form = UpdateUserForm(initial={ 
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        })
    else:
        form = UpdateUserForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            fname = data['first_name']
            lname = data['last_name']
            email = data['email']

            user.first_name = fname
            user.last_name = lname
            user.email = email
            user.save()
            if posts_redirect == 'false':
                return HttpResponseRedirect(reverse('admin_pages:admin_index'))
            else:
                return HttpResponseRedirect(reverse('admin_pages:manage_posts'))

    context = { 'form': form }
    return render(request, 'users/update_user.html', context)


@otp_required
def confirm_delete_user(request, user_id):
    """Display a confirmation dialog view before deleting a user."""
    user = User.objects.get(id=user_id)

    context = { 'user': user }
    return render(request, 'users/confirm_delete_user.html', context)


@otp_required
def delete_user(request, user_id):
    """Delete the user."""
    User.objects.get(id=user_id).delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_users'))
