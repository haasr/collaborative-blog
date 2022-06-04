from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.models import Site

from django.core.files.storage import default_storage
from django.core.exceptions import MultipleObjectsReturned
from django.views.decorators.cache import never_cache
from django_otp.decorators import otp_required
from django.utils.timezone import make_aware as timezone_make_aware

from mail_subscription.models import EmailSubscriber
from mail_subscription.newsletters import newsletter_scheduler

from site_pages_forms import form_sender

from custom_decorators.decorators import is_superuser
from .models import *
from .forms import *

from datetime import datetime as dt, timedelta
import json
import os


POSTS_IMGS_DIR  = 'site_pages/posts/images/'
TOPICS_IMGS_DIR = 'site_pages/topics/topic_splash_images/'


def get_topics():
    return [ t for t in Topic.objects.all() ]


@login_required
@staff_member_required
def admin_index(request):
    """This function and the manage_posts function do not require OTP. Rather
    template logic provides the user the options to set up OTP (and nothing else)
    before they are able to see the proper view. This way users are able to do
    initial setup of two-factor authentication as well as reset and reconfigure
    it. If the user is superuser and 2FA is set up, they will be provided the
    administrative menu template. Otherwise, they will be directed to the posts
    management template where they will see their authored posts + the posts they
    have been added as a collaborator on.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on their superuser status.
    """
    context = { 'current_user': request.user.first_name }

    if request.user.is_superuser:
        return render(request, 'admin_pages/index.html', context)
    else:
        return HttpResponseRedirect(reverse('admin_pages:manage_posts'))


@is_superuser
@otp_required
def manage_site_look(request):
    """
    Provides the user a form template to edit the data of the SiteLook object
    -- for settings including which pages are shown, what information appears
    in the footer, and the font and favicon -- with id 1.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    site_look = SiteLook.objects.get(id=1)

    if (request.method != 'POST'):
        form = SiteLookForm(instance=site_look)
    else:
        form = SiteLookForm(instance=site_look, data=request.POST)

    if form.is_valid():
        form.save()

        if len(request.FILES) != 0:
            if 'navigation_img' in request.FILES.keys():
                image = request.FILES['navigation_img']
                image.name = 'nav_image.png'
                u = S3NavUpload(file=image)
                u.save()

            if 'favicon' in request.FILES.keys():
                image = request.FILES['favicon']
                image.name = 'favicon.ico'
                u = S3FaviconUpload(file=image)
                u.save()

        return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_site_look/manage_site_look.html', context)


@is_superuser
@otp_required
def manage_home(request):
    """Provides the user a form template to edit the data of the Home
    object (for landing page content) with id 1.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """

    home = Home.objects.get(id=1)

    if request.method != 'POST':
        # no data submitted; createVIDEOS blank form.
        form = HomeForm(instance=home)
    else:
        form = HomeForm(instance=home, data=request.POST)

        if form.is_valid():
            form.save()

            if (len(request.FILES) != 0):
                image = request.FILES['background_img']
                image.name='background.png'
                u = S3HomeBackgroundUpload(file=image)
                u.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_home/manage_home.html', context)


@is_superuser
@otp_required
def manage_topics_header(request):
    """Provides the user a form template to edit the data of the Topics
    object with id 1. The Topics object simply has options for the topics
    header (as opposed to a Topic object, which is a single topic which may
    be associated with Post objects).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    topics = Topics.objects.get(id=1)

    if request.method != 'POST':
        form = TopicsPageForm(instance=topics)
    else:
        form = TopicsPageForm(instance=topics, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                image = request.FILES['header_image']
                image.name = 'topics-header' + os.path.splitext(image.name)[1]
                u = S3TopicsHeaderUpload(file=image)
                u.save()
                topics.header_image_file_name = image.name
                topics.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_topics/manage_topics_header.html', context)


@is_superuser
@otp_required
def manage_about(request):
    """Provides the user a form template to edit the data of the About
    object (for About page content) with id 1. The About object determines
    the content of the about page (and in turn, it's layout).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    about = About.objects.get(id=1)

    if (request.method != 'POST'):
        form = AboutForm(instance=about)
    else:
        form = AboutForm(instance=about, data=request.POST)

        if form.is_valid():
            form.save()
            if (len(request.FILES) != 0):
                if('header_image' in request.FILES):
                    image = request.FILES['header_image']
                    image.name = 'about-header' + os.path.splitext(image.name)[1]
                    u = S3AboutHeaderUpload(file=image)
                    u.save()
                    about.header_image_file_name = image.name
                if ('box1_img' in request.FILES):
                    image = request.FILES['box1_img']
                    image.name = 'about-box1-img' + os.path.splitext(image.name)[1]
                    u = S3AboutBox1Upload(file=image)
                    u.save()
                    about.box1_img_file_name = image.name
                if ('box2_img' in request.FILES):
                    image = request.FILES['box2_img']
                    image.name = 'about-box2-img' + os.path.splitext(image.name)[1]
                    u = S3AboutBox2Upload(file=image)
                    u.save()
                    about.box2_img_file_name = image.name
            about.save()
            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_about/manage_about.html', context)


@is_superuser
@otp_required
def manage_contact(request):
    """Provides the user a form template to edit the data of the Contact
    object (for Contact page content) with id 1. The Contact object determines
    the information displayed on the contact page (and in turn, the page's layout).

    Parameters:
    request (WSGIRequest): An HTTP Request object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    contact = Contact.objects.get(id=1)

    if request.method != 'POST':
        form = ContactForm(instance=contact)
    else:
        form = ContactForm(instance=contact, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                if 'header_image' in request.FILES:
                    image = request.FILES['header_image']
                    image.name = 'contact-header' + os.path.splitext(image.name)[1]
                    u = S3ContactHeaderUpload(file=image)
                    u.save()
                    contact.header_image_file_name = image.name
                    contact.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'contact': contact, 'form': form }
    return render(request, 'admin_pages/manage_contact/manage_contact.html', context)


@is_superuser
@otp_required
def manage_contrib(request):
    """Provides the user a form template to edit the data of the Contrib
    object (for Contribute page content) with id 1.

    Parameters:
    request (WSGIRequest): An HTTP Request object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    contrib = Contrib.objects.get(id=1)

    if request.method != 'POST':
        form = ContribForm(instance=contrib)
    else:
        form = ContribForm(instance=contrib, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                if 'header_image' in request.FILES:
                    image = request.FILES['header_image']
                    image.name = 'contrib-header' + os.path.splitext(image.name)[1]
                    u = S3ContactHeaderUpload(file=image)
                    u.save()
                    contrib.header_image_file_name = image.name
                    contrib.save()

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'contrib': contrib, 'form': form }
    return render(request, 'admin_pages/manage_contrib/manage_contrib.html', context)


@login_required
@staff_member_required
def manage_posts(request):
    """This function and the admin_index function do not require OTP. Rather
    template logic provides the user the options to set up OTP (and nothing else)
    before they are able to see the proper view. This way users are able to do
    initial setup of two-factor authentication as well as reset and reconfigure
    it. If the user does have 2FA set up, they will be provided a posts management
    screen to conveniently manage their posts and their topics. Staff (standard)
    users get to access their authored posts and posts shared with them for
    collaboration. Admins get to access those and all posts that are public. Admins
    do not get to see private or restricted posts that they do not author or
    collaborate on.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    author = AuthorProfile.objects.get(user=request.user)

    collaborators = PostCollaborator.objects.all()
    posts = Post.objects.all().order_by('-date')

    collab_posts = []
    author_posts = None

    for c in collaborators:
        if c.author == author:
            collab_posts.append(c.post)

    author_posts = posts.filter(author=author)

    topics = Topic.objects.all()

    context = {
        'profile': author,
        'public_posts': posts.filter(visibility='public'),
        'author_posts': author_posts,
        'collab_posts': collab_posts,
        'collaborators': collaborators,
        'topics': topics
    }
    if not request.user.is_superuser:
        return render(request, 'admin_pages/manage_posts/manage_posts.html', context)
    else:
        return render(request, 'admin_pages/manage_posts/manage_posts_admin.html', context)


@otp_required
@staff_member_required
def new_post(request):
    """Provides the user a form template to create a new Post object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    author = AuthorProfile.objects.get(user=request.user)
    post = Post(title='', author=author)
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            post.refresh_from_db()
            try:
                if len(request.FILES) != 0:
                    image = request.FILES['box_img']
                    s = post.slug[:50] # AWS allows up to 76 chars including .ext -- too long anyway.
                    image.name = 'post-' + s + os.path.splitext(image.name)[1]
                    u = S3PostsUpload(file=image)
                    u.save()
                    post.box_img_file_name = image.name
                    post.save()
            except MultipleObjectsReturned:
                form.add_error(None, 'The title must be unique')
                post.delete() # Delete the post that was recently saved
                return render(request, 'admin_pages/manage_posts/posts/new_post.html', { 'form': form }) # Go back to template (try again!)

            return redirect('admin_pages:add_topic', post_id=post.id)

    return render(request, 'admin_pages/manage_posts/posts/new_post.html', { 'form': form }) # Go back to template (try again!)


@otp_required
@staff_member_required
def edit_post(request, post_id):
    """Provides the user a form template to edit an existing Post object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_id (int): The public key of the Post to be edited.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    post = Post.objects.get(id=post_id)
    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                s = post.slug[:50] # AWS allows up to 76 chars including .ext -- too long anyway.
                image = request.FILES['box_img']
                image.name = 'post-' + s + os.path.splitext(image.name)[1]
                u = S3PostsUpload(file=image)
                u.save()
                post.box_img_file_name = image.name
                post.save()

            return HttpResponseRedirect(reverse('admin_pages:manage_posts'))

    context = {'form': form, 'post_id': post.id }
    return render(request, 'admin_pages/manage_posts/posts/edit_post.html', context)


@otp_required
@staff_member_required
def replace_post_image(request, post_id):
    """Provides the user a form template to select an image to use for the Post.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_id (int): The public key of the Post to be edited.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    post = Post.objects.get(id=post_id)

    if request.method != 'POST':
        form = PostImageForm(instance=post)
    else:
        form = PostImageForm(instance=post, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                s = post.slug[:50] # AWS allows up to 76 chars including .ext -- too long anyway.
                image = request.FILES['box_img']
                image.name = 'post-' + s + os.path.splitext(image.name)[1]
                u = S3PostsUpload(file=image)
                u.save()
                post.box_img_file_name = image.name
                post.save()

            return HttpResponseRedirect(reverse('admin_pages:manage_posts'))

    context = {'form': form, 'post': post }
    return render(request, 'admin_pages/manage_posts/posts/replace_post_image.html', context)


@otp_required
@staff_member_required
def confirm_delete_post(request, post_id):
    """Provides a view to confirm or cancel the deletion of the Post with ID post_id.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_id (int): The PK of the Post object to delete, if deletion is confirmed.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    context = { 'post_id': post_id }
    return render(request, 'admin_pages/manage_posts/posts/confirm_delete_post.html', context)


@otp_required
@staff_member_required
def delete_post(request, post_id):
    """Deletes an existing Post object and its associated cover image.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    denylistemail_id (int): The PK of the Post object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    post = Post.objects.get(id=post_id)
    default_storage.delete(POSTS_IMGS_DIR + post.box_img_file_name)
    post.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_posts'))


 # I found a nasty error after deleting a user account that had
 # previously been associated with an AuthorProfile where the author
 # had been a collaborator. An old collaborator was cached (even after)
 # multiple sign-outs, sign-ins and saving the form put it in an error
 # state since the old AuthorProfile ID no longer existed. Hence never_cache
 # to the rescue.
@never_cache
@otp_required
@staff_member_required
def manage_post_collaborators(request, post_id):
    """Provides a form template for selecting which authors are collaborators
    on a Post. When the form is POSTed, all PostCollaborators associated with
    the Post are deleted and then the selected PostCollaborators are added (that
    guarantees that if someone previously designated as a collaborator were
    unchecked, that their PostCollaborator object would be deleted).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    post = Post.objects.get(id=post_id)
    post_collaborators = PostCollaborator.objects.filter(post=post)
    author = AuthorProfile.objects.get(user=request.user)

    authors_sel_ids = []
    for p in post_collaborators:
        authors_sel_ids.append(p.author.id)

    if request.method != 'POST':
        form = PostCollabForm(author=author)
    else:
        form = PostCollabForm(author=author, data=request.POST)

        if form.is_valid():
            post_collaborators.delete()
            for author_id in form.cleaned_data['collab_choices']:
                pc = PostCollaborator(post=post, author=AuthorProfile.objects.get(id=author_id))
                pc.save()

            return HttpResponseRedirect(reverse('admin_pages:manage_posts'))

    author = AuthorProfile.objects.get(user=request.user)

    context = {
        'post_id': post.id,
        'authors_selected': json.dumps(authors_sel_ids),
        'author_id': author.id,
        'form': form
    }
    return render(request, 'admin_pages/manage_posts/collaborators/manage_collaborators.html', context)


@otp_required
@staff_member_required
def delete_post_topic(request, post_id, topic_id):
    """Removes a Topic specified by topic_id from the specified Post's collection
    of Topics.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_id (int): The PK of the Post object from which the Topic will be disassociated.
    topic_id (int): The PK of the Topic object

    Returns:
    HttpResponseRedirect: Directs the user to the appropriate URL.
    """
    post = Post.objects.get(id=post_id)
    post.topics.remove(Topic.objects.get(id=topic_id))
    return HttpResponseRedirect(reverse('admin_pages:manage_posts'))


@never_cache
@otp_required
@staff_member_required
def add_topic(request, post_id):
    """Allows the user to add a new or existing topic to the specified Post.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_id (int): The PK of the Post object to which the Topic will be associated.

    Returns:
    HttpResponseRedirect: Directs the user to the appropriate URL.
    """
    post = Post.objects.get(id=post_id)

    if request.method != 'POST':
        form = AddTopicForm()
    else:
        form = AddTopicForm(data=request.POST)
        if form.is_valid():
            name = form.data['name'].upper()

            existing = False
            for topic in get_topics():
                if name == topic.name:
                    existing = True
                    break

            if not existing:
                topic = Topic(name=name)
                topic.save()

            post.topics.add(topic)
            return HttpResponseRedirect(reverse('admin_pages:manage_posts'))

    context = { 'form': form, 'post_id': post.id }
    return render(request, 'admin_pages/manage_posts/topics/add_topic.html', context)


@is_superuser
@otp_required
def manage_topics(request):
    """Provides a view for managing each Topic. Topic names can be edited or deleted;
    marking them as 'featured' will link them in a large centered area on the topics
    page. Each topic can also have an uploaded background image associated with it
    that shows up behind the topic link of a featured topic. Also links to the form
    for managing the topics page header (using the manage_topics_header function).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    topics = Topic.objects.all().order_by('name')
    context = { 'topics': topics }
    return render(request, 'admin_pages/manage_topics/manage_topics.html', context)


@is_superuser
@otp_required
def edit_topic(request, topic_id):
    """Provides the user a form template to edit an existing Topic object. This includes
    the ability to set a splash image for the topic that will show up on the topics page
    if the Topic is marked as featured.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    topic_id (int): The public key of the Topic to be edited.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        form = TopicForm(instance=topic)
    else:
        form = TopicForm(instance=topic, data=request.POST)
        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                image = request.FILES['splash_img']
                # Replace space char w/ underscore for S3 file-naming convention.
                # If this were not done, then templates tries to render image w/
                # space in filename (%29) but AWS has replaced the space with _
                # in the bucket so the image would not be found:
                topic_name = topic.name.replace(' ', '_')
                image.name = topic_name + '-splash-img' + os.path.splitext(image.name)[1]
                u = S3TopicsUpload(file=image)
                u.save()
                topic.splash_img_file_name = image.name
                topic.save()

            return HttpResponseRedirect(reverse('admin_pages:manage_topics'))

    context = { 'form': form, 'topic_id': topic.id }
    return render(request, 'admin_pages/manage_topics/edit_topic.html', context)


@is_superuser
@otp_required
def confirm_delete_topic(request, topic_id):
    """Provides a view to confirm or cancel the deletion of the Topic with ID topic_id.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_id (int): The PK of the Topic object to delete, if deletion is confirmed.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    context = { 'topic_id': topic_id }
    return render(request, 'admin_pages/manage_topics/confirm_delete_topic.html', context)


@is_superuser
@otp_required
def delete_topic(request, topic_id):
    """Deletes the topic of the specified ID.

    Parameters:
    request (WSGIRequest): An HTTPRequest object.
    topic_id (int): The ID of the topic to be deleted.

    Returns HttpResponseRedirect: Directs the user back to the Manage Topics Page.
    """
    topic = Topic.objects.get(id=topic_id)
    default_storage.delete(TOPICS_IMGS_DIR + topic.splash_img_file_name)
    topic.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_topics'))


@is_superuser
@otp_required
def manage_seo(request):
    """Provides the user a form template to edit the data of the SEO
    object (for--well--SEO) with id 1.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    seo = SEO.objects.get(id=1)

    if request.method != 'POST':
        form = SEOForm(instance=seo)
    else:
        form = SEOForm(instance=seo, data=request.POST)

        if form.is_valid():
            form.save()

            site = Site.objects.get(id=1)
            site.name=seo.meta_title
            site.save() # Site name matches meta title

            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'seo': seo, 'form': form }
    return render(request, 'admin_pages/manage_seo/manage_seo.html', context)


@otp_required
def manage_author_profile(request, posts_redirect):
    """Provides the user a form template to edit the AuthorProfile linked to their account.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    posts_redirect (str): 'true' will redirect to the Manage Posts page. 'false' will redirect ot the Admin Index page.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    profile = AuthorProfile.objects.get(user=User.objects.get(id=request.user.id))

    if request.method != 'POST':
        form = AuthorProfileForm(instance=profile)
    else:
        form = AuthorProfileForm(instance=profile, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                icon = request.FILES['profile_icon']
                icon.name = 'profile-icon-' + str(profile.id) + os.path.splitext(icon.name)[1]
                u = S3AuthorProfileUpload(file=icon)
                u.save()
                profile.profile_icon_file_name = icon.name
                profile.save()

            if posts_redirect == 'false':
                return HttpResponseRedirect(reverse('admin_pages:admin_index'))
            else:
                return HttpResponseRedirect(reverse('admin_pages:manage_posts'))

    context = { 'profile': profile, 'form': form }
    if posts_redirect == 'false':
        return render(request, 'admin_pages/manage_author_profile/manage_author_profile.html', context)
    else:
        return render(request, 'admin_pages/manage_author_profile/manage_author_profile_posts_redirect.html', context)


@is_superuser
@otp_required
def manage_users(request):
    """Provides the user a form template to facilitate creation and deletion of a
    User staff or admin (superuser) account.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    # Without order_by, order was being changed based on admin status...it was weird.
    users = User.objects.exclude(id=request.user.id).order_by('first_name')

    context = { 'users': users }
    return render(request, 'admin_pages/manage_users/manage_users.html', context)


@is_superuser
@otp_required
def toggle_superuser_status(request, user_id):
    """Toggles the boolean, is_superuser, of the specified User object, thereby
    changing what pages the user has access to.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    user_id (int): The PK of the User object to change admin permission on.

    Returns:
    HttpResponse: Returns a status code indicating that the request succeeded.
    """
    u = User.objects.get(id=user_id)
    if u.is_superuser:
        u.is_superuser = False
    else:
        u.is_superuser = True
    u.save()

    return HttpResponse(status=204)


@is_superuser
@otp_required
def manage_email_account(request):
    """Provides the user a form template to edit the EmailAccount object
    with id 1. The object's single email_addr field will contain the
    email address of the recipient for site_pages.form_sender which will
    send form data as an email.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    email_account = EmailAccount.objects.get(id=1)

    if (request.method != 'POST'):
        form = EmailAccountForm(instance=email_account)
    else:
        form = EmailAccountForm(instance=email_account, data=request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'email_account': email_account, 'form': form }
    return render(request, 'admin_pages/manage_email/manage_email.html', context)


@is_superuser
@otp_required
def manage_email_denylist(request):
    """Provides the user a template to control the contents of the list of
    email addresses which site_pages.views will check against an email address
    in a submitted form before emailing that form data to the recipient address
    such that if the address is listed, the form data will not be emailed.
    Allows CRUD operations for the DenylistEmailModel objects.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    denylist_emails = DenylistEmail.objects.all()
    context = { 'denylist_emails': denylist_emails }
    return render(request, 'admin_pages/manage_denylists/manage_email_denylist.html', context)


@is_superuser
@otp_required
def new_denylistemail(request):
    """Provides the user a form template to create a new DenylistEmailModel object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    if request.method != 'POST':
        form = DenylistEmailForm()
    else:
        form = DenylistEmailForm(data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_pages:manage_email_denylist'))

    context = { 'form': form }
    return render(request, 'admin_pages/manage_denylists/denylistemails/new_denylistemail.html', context)


@is_superuser
@otp_required
def edit_denylistemail(request, denylistemail_id):
    """Provides the user a form template to edit an existing DenylistEmailModel object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    denylistemail_id (int): The public key of the DenyListEmail to edit

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the validity of the form.
    """
    denylistemail = DenylistEmail.objects.get(id=denylistemail_id)

    if (request.method != 'POST'):
        form = DenylistEmailForm(instance=denylistemail)
    else:
        form = DenylistEmailForm(instance=denylistemail, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'admin_pages:manage_email_denylist'
            ))

    context = { 'denylistemail': denylistemail, 'form': form }
    return render(request, 'admin_pages/manage_denylists/denylistemails/edit_denylistemail.html', context)


@is_superuser
@otp_required
def delete_denylistemail(request, denylistemail_id):
    """Deletes an existing DenylistEmailModel object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    denylistemail_id (int): The PK of the DenylistEmailModel object to delete.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    DenylistEmail.objects.get(id=denylistemail_id).delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_email_denylist'))


@is_superuser
@otp_required
def manage_viewer_contact_form_settings(request):
    contact = Contact.objects.get(id=1)

    if request.method != 'POST':
        form = ViewerContactFormSettingsForm(instance=contact)
    else:
        form = ViewerContactFormSettingsForm(instance=contact, data=request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    descr =  (
        'This form appears on the Contact page when \"Show Form\" is checked'
        ' and the Contact page is showing.'
    )

    context = {
        'form_title': 'Contact Form',
        'form_description': descr,
        'form': form
    }
    return render(request, 'admin_pages/manage_site_pages_forms/manage_form_generic.html', context)


@is_superuser
@otp_required
def manage_email_contact_form_settings(request):
    """Provides a form for managing the settings for the email contact form
    that appears in the page footer.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    settings = EmailContactFormSettings.objects.get(id=1)

    if request.method != 'POST':
        form = EmailContactFormSettingsForm(instance=settings)
    else:
        form = EmailContactFormSettingsForm(instance=settings, data=request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    descr = (
        'This form appears in your site footer when \"Show Form\" is checked.'
    )

    context = {
        'form_title': 'Email Contact Form',
        'form_description': descr,
        'form': form
    }
    return render(request, 'admin_pages/manage_site_pages_forms/manage_form_generic.html', context)


@is_superuser
@otp_required
def manage_contribute_form_settings(request):
    """Provides a form for managing the settings for the contribute form that appears
    on the contribute page.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """

    contrib = Contrib.objects.get(id=1)

    if request.method != 'POST':
        form = ContributeFormSettingsForm(instance=contrib)
    else:
        form = ContributeFormSettingsForm(instance=contrib, data=request.POST)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('admin_pages:admin_index'))


    descr = (
        'This form appears on the Contribute page when the page is made'
        ' visible.'
    )

    context = {
        'form_title': 'Contribute Form',
        'form_description': descr,
        'form': form
    }
    return render(request, 'admin_pages/manage_site_pages_forms/manage_form_generic.html', context)


@is_superuser
@otp_required
def manage_subscribe_form_settings(request):
    """Provides a form for managing the settings for the subscribe form that
    appears when email newsletters are enabled.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    settings = SubscribeFormSettings.objects.get(id=1)

    if request.method != 'POST':
        form = SubscribeFormSettingsForm(instance=settings)
    else:
        form = SubscribeFormSettingsForm(instance=settings, data=request.POST)

        if form.is_valid():
            form.save()

            if len(request.FILES) != 0:
                image = request.FILES['box_img']
                image.name = 'subscribe-form' + os.path.splitext(image.name)[1]

                u = S3SubscribeFormBoxImgUpload(file=image)
                u.save()

                settings.box_img_file_name = image.name
                settings.save()

            newsletter_scheduler.update_newsletter()
            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    descr = (
        'This form appears once per session as a popup asking the user'
        ' to subscribe to the newsletter.'
    )

    context = {
        'form_title': 'Subscribe Form',
        'form_description': descr,
        'form': form
    }
    return render(request, 'admin_pages/manage_site_pages_forms/manage_form_generic.html', context)


@is_superuser
@otp_required
def manage_subscriber_newsletter(request):
    """Provides a form for managing the settings for the subscriber newsletter
    that will get emailed out to email subscribers (i.e., the collection of
    mail_subscription.models.EmailSubscriber objects stored in the system).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    newsletter = SubscriberNewsletter.objects.get(id=1)

    if request.method != 'POST':
        form = SubscriberNewsletterForm(instance=newsletter)
    else:
        form = SubscriberNewsletterForm(instance=newsletter, data=request.POST)
        if form.is_valid():
            form.save()
            # Build full unsubscribe URL:
            newsletter.unsubscribe_url = newsletter.site_url.rstrip('/') + '/mail/unsubscribe/'
            newsletter.save()
            newsletter_scheduler.update_newsletter()
            return HttpResponseRedirect(reverse('admin_pages:admin_index'))

    context = { 'form': form }

    return render(request, 'admin_pages/manage_subscriber_newsletter/manage_newsletter/manage_newsletter.html',
                    context)


@is_superuser
@otp_required
def manage_subscribers(request):
    """Provides the user a template to view and manage each EmailSubscriber
    object (the model for which is in mail_subscription.models).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    subscribers = EmailSubscriber.objects.all()

    context = { 'subscribers': subscribers }

    return render(request, 'admin_pages/manage_subscriber_newsletter/manage_subscribers/manage_subscribers.html',
                    context)


@is_superuser
@otp_required
def confirm_delete_subscriber(request, subscriber_email):
    """Provides a view to confirm or cancel the deletion of the EmailSubscriber with
    the email address, subscriber_email.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    subscriber_email (str): The unique email address of the EmailSubscriber to delete, if deletion is confirmed.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    context = { 'subscriber_email': subscriber_email }
    return render(request, 'admin_pages/manage_subscriber_newsletter/manage_subscribers/confirm_delete_subscriber.html',
                    context)


@is_superuser
@otp_required
def delete_subscriber(request, subscriber_email):
    """Deletes an existing EmailSubscriber object (for which the model is in mail_subscription.models).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    subscriber_email (str): The unique email address of the EmailSubscriber to delete, if deletion is confirmed.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    sub = EmailSubscriber.objects.get(email_addr=subscriber_email)
    sub.delete()

    return HttpResponseRedirect(reverse('admin_pages:manage_subscribers'))


@is_superuser
@otp_required
def manage_mail_send_failures(request, days=30):
    """Provides a view for managing each instance of a FormSendFailure or
    a NewsletterSendFailure. It also facilitates visualization of the
    failures by the form name or newsletter type and allows for the
    user to attempt resending the form data of a FormSendFailure instance.
    The number of days chosen determines what objects will be returned.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    days (int): A range from the number of days - 1 before the present day
    to the present day for which the failure objects returned will match this timerange.

    Returns:
    HttpResponse: Directs the user to the appropriate URL depending on the request method.
    """
    now_naive = dt.now()
    # Converts to non-naive datetime by adding timezone. -- Uses timezone spec. in settings.
    # (prevents warning similar to https://stackoverflow.com/questions/18622007/runtimewarning-datetimefield-received-a-naive-datetime)
    now = timezone_make_aware(now_naive)
    time_gt = now - timedelta(days=(days-1))

    form_send_failures = FormSendFailure.objects.filter(timestamp__gt=time_gt).order_by('-timestamp')
    newsletter_send_failures = NewsletterSendFailure.objects.filter(timestamp__gt=time_gt).order_by('-timestamp')

    form_failures_list = list(form_send_failures.values_list('form_name', flat=True))
    form_failures_dict = {}
    nl_failures_list = list(newsletter_send_failures.values_list('template_used', flat=True))
    nl_failures_dict = {}

    for item in form_failures_list:
        try:
            form_failures_dict[item] += 1
        except:
            form_failures_dict[item] = 1

    for item in nl_failures_list:
        try:
            nl_failures_dict[item] += 1
        except:
            nl_failures_dict[item] = 1

    form_failures_xlabels = list(form_failures_dict.keys())
    form_failures_data = list(form_failures_dict.values())

    nl_failures_xlabels = list(nl_failures_dict.keys())
    nl_failures_data = list(nl_failures_dict.values())

    context = {
        'form_send_failures': form_send_failures,
        'newsletter_send_failures': newsletter_send_failures,
        'form_failures_data': json.dumps(form_failures_data),
        'form_failures_xlabels': json.dumps(form_failures_xlabels),
        'newsletter_failures_xlabels': json.dumps(nl_failures_xlabels),
        'newsletter_failures_data': json.dumps(nl_failures_data),
        'timerange': days
    }

    return render(request, 'admin_pages/manage_mail_send_failures/manage_mail_send_failures.html', context)


@is_superuser
@otp_required

def delete_form_send_failure(request, failure_id):
    """Deletes an existing FormSendFailure object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    failure_id (int): The PK of the FormSendFailure to be deleted.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    f = FormSendFailure.objects.get(id=failure_id)
    f.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_mail_send_failures'))


@is_superuser
@otp_required
def delete_newsletter_send_failure(request, failure_id):
    """Deletes an existing NewsletterSendFailure object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    failure_id (int): The PK of the NewsletterSendFailure to be deleted.

    Returns:
    HttpResponse: Directs the user to the appropriate URL.
    """
    f = NewsletterSendFailure.objects.get(id=failure_id)
    f.delete()
    return HttpResponseRedirect(reverse('admin_pages:manage_mail_send_failures'))


@is_superuser
@otp_required
def resend_form_email(request):
    """Calls on the site_pages_forms.form_sender module's resend_form_failure
    function to attempt to resend the form data which previously failed. The
    method acquires the necessary parameters from the POST request.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns:
    HttpResponse: Returns the appropriate status code indicating success, failure, or not allowed.
    """
    if request.method == 'POST':
        try:
            form_data = eval(request.POST['form_data'])
            to = request.POST['to']
            form_name = request.POST['form_name']

            success = form_sender.resend_form_email(form_data, to, form_name)
            if success == 1:
                failure = FormSendFailure.objects.get(id=int(request.POST['form_id']))
                failure.resent_ok = True
                failure.save()
                return HttpResponse(200)
            else:
                return HttpResponse(400)
        except:
            return HttpResponse(400)
    else:
        return HttpResponse(403)