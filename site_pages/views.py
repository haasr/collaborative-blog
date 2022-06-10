from django.shortcuts import render

from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required
from django_otp.decorators import otp_required
from django.urls import reverse

from admin_pages.models import *
from admin_pages.forms import CommentForm
from site_pages_forms.forms import ContributeForm, ViewerContactForm
from .forms import *


city = 'None'

sitelook = SiteLook.objects.get(id=1)

MONTHS = [
    [ 'January', 'February', 'March' ],
    [ 'April', 'May', 'June' ],
    [ 'July', 'August', 'September' ],
    [ 'October', 'November', 'December' ]
]

MONTHS_DICT = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12
}


def handle_404(request, exception):
    """Renders custom 404 template when a 404 error is encountered.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the 404 template.
    """
    return render(request, '404.html', status=404)


def show_subscribe_form(request):
    """Checks the cookies in the request object passed to see if
    'subscribe_form_shown' exists (and if so, if it is true). If the
    'subscribe_form_shown' value is True, the function returns False,
    indicating not to show the subscribe form and else it returns True,
    indicating to show the subscribe form.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    bool: False if request.COOKIES['subscribe_form_shown'] exists and is True.
    bool: True otherwise.
    """
    if request.COOKIES.get('subscribe_form_shown'):
       return False
    else:
        return True


def index(request):
    """Renders the home/index page.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the index template.
    """
    sitelook.refresh_from_db()
    home = Home.objects.get(id=1)

    posts = Post.objects.filter(visibility='public').order_by('-date')
    featured_posts = posts.filter(is_featured=True)
    posts = posts[0:6] # Only accumulate up to 6 most recent

    context = { 
        'home': home, 
        'posts': posts,
        'featured_posts': featured_posts,
    }

    response = render(request, 'site_pages/index.html', context)
    return response


def post(request, post_slug, goto_section=''):
    """Renders a Post and its associated threads of comments if it is public or
    if the requester is an authenticated user with the appropriate access.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_slug (str): The unique slug that identifies the post to be loaded.
    goto_section (str): The section of the page to be navigated to on load, when that section's ID matches this paramater value.

    Returns
    HttpResponse: Directs the user to the post template.
    """
    post = Post.objects.get(slug=post_slug)
    threads = Thread.objects.filter(post=post).order_by('-og_date')
    comments = Comment.objects.filter(post_id=post.id).order_by('og_date')

    post_collaborators = PostCollaborator.objects.filter(post=post)
    has_collaborators = True if len(post_collaborators) != 0 else False
    user = request.user
    context = {
        'post': post,
        'goto_section': goto_section,
        'threads': threads,
        'comments': comments,
        'post_collaborators': post_collaborators,
        'has_collaborators': has_collaborators,
    }
    response = None

    if post.visibility == 'public':
        context['show_subscribe_form'] = show_subscribe_form(request)

        response = render(request, 'site_pages/post.html', context)
        response.set_cookie('subscribe_form_shown', True)

    elif post.visibility == 'private':
        if user.is_authenticated and (user.id == post.author.user.id):
            response = render(request, 'site_pages/post.html', context)
        else:
            response = HttpResponseRedirect(reverse('login'))

    elif post.visibility == 'restrict':
        if user.is_authenticated:
            is_allowed = user.is_superuser
            if post.author.user.id == request.user.id:
                is_allowed = True # If the requester is the author
            else:
                for c in post_collaborators:
                    if c.author.user.id == user.id:
                        is_allowed = True
                        break
            if is_allowed:
                context['show_subscribe_form'] = show_subscribe_form(request)

                response = render(request, 'site_pages/post.html', context)
                response.set_cookie('subscribe_form_shown', True)

                return response
            else:
                response = HttpResponseRedirect(reverse('index'))
        else:
            response = HttpResponseRedirect(reverse('login'))

    else:
        response =  HttpResponseRedirect(reverse('index'))

    return response


def post_comment_new_thread(request, post_slug):
    """Allows the requester to create a Comment object related to a new
    Thread (admin_pages.models.Thread, not a thread of execution).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_slug (str): The unique slug that identifies the Post to which the thread
    will belong and is used to redirect back to the correct post page.

    Returns
    HttpResponse: Directs the user to the correct template.
    """
    post=Post.objects.get(slug=post_slug)
    comment = Comment(post_id=post.id, orig=True)
    post_slug = post.slug
    
    if request.method != 'POST':
        if request.user:
            author = AuthorProfile.objects.get(user=request.user)
            comment.name = author.preferred_name

        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            if form.cleaned_data['text'] == '': # Don't save -- no text!
                return HttpResponseRedirect(reverse('post', args=[post_slug]))

            thread = Thread(post=post)
            thread.save()
            comment.thread = thread

            form.save()

            return HttpResponseRedirect(reverse('post', args=[post_slug, 'post-comments']))
        else:
            print(form.errors)

    context = {
        'post_slug': post_slug,
        'form': form,
    }
    print('Returning form')
    return render(request, 'site_pages/comment.html', context)



def post_comment_existing_thread(request, post_slug, thread_id):
    """Allows the requestor to create a Comment object related to an
    existing Thread object.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_slug (str): The unique slug that identifies the Post to which the thread
    belongs and is used to redirect back to the correct post page.

    Returns
    HttpResponse: Directs the user to the correct template.
    """
    thread = Thread.objects.get(id=thread_id)
    comment = Comment(post_id=thread.post.id)
    
    if request.method != 'POST':
        if request.user:
            author = AuthorProfile.objects.get(user=request.user)
            comment.name = author.preferred_name

        form = CommentForm(instance=comment)
    else:
        form = CommentForm(instance=comment, data=request.POST)
        if form.is_valid():
            if form.cleaned_data['text'] == '': # Don't save -- no text!
                return HttpResponseRedirect(reverse('post', args=[post_slug]))
            
            comment.thread = thread
            form.save()

        return HttpResponseRedirect(reverse('post', args=[post_slug, 'post-comments']))

    context = {
        'post_slug': post_slug,
        'thread_id': thread.id,
        'form': form,
    }
    return render(request, 'site_pages/comment.html', context)


def topics(request):
    """Renders the topics page if the Sitelook object with ID 1
    has a value of True for 'show_topics' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_topics:
        topics_header = Topics.objects.get(id=1)
        topics = Topic.objects.all().order_by('name')

        context = {
            'topics_header': topics_header,
            'topics': topics
        }

        context['show_subscribe_form'] = show_subscribe_form(request)

        response = render(request, 'site_pages/topics.html', context)
        response.set_cookie('subscribe_form_shown', True)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def topic_posts(request, topic_id):
    """Renders the topic_posts page where the 5 most recent public posts of the
    specified topic as well as all the public posts of the specified topic are
    displayed.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    topic_id (int): The PK of the Topic for which Posts should be shown if they have this Topic.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    topic = Topic.objects.get(id=topic_id)
    posts = Post.objects.filter(visibility='public').order_by('-date')
    topic_posts = []

    topic_name_normalized = ''
    t = topic.name.split(' ')
    for _ in t:
        topic_name_normalized += _[0] + _[1:].lower() + ' '

    topic_name_normalized = topic_name_normalized.rstrip(' ')

    for p in posts:
        for t in p.topics.all():
            if t.id == topic_id:
                topic_posts.append(p)

    context = {
        'topic_name_normalized': topic_name_normalized,
        'recent_posts': topic_posts[:5],
        'posts': topic_posts
    }

    context['show_subscribe_form'] = show_subscribe_form(request)

    response = render(request, 'site_pages/topic_posts.html', context)
    response.set_cookie('subscribe_form_shown', True)

    return response


def contact(request):
    """Renders the contact page if the Sitelook object with ID 1
    has a value of True for 'show_contact' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_contact:
        contact = Contact.objects.get(id=1)
        form = ViewerContactForm()

        context = {
            'contact': contact,
            'viewer_contact_form': form
        }

        response = render(request, 'site_pages/contact.html', context)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def contrib(request):
    """Renders the topic page if the Sitelook object with ID 1
    has a value of True for 'show_topics' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_contrib:
        contrib = Contrib.objects.get(id=1)
        form = ContributeForm()

        context = { 'contrib': contrib, 'contrib_form': form }

        context['show_subscribe_form'] = show_subscribe_form(request)

        response = render(request, 'site_pages/contribute.html', context)
        response.set_cookie('subscribe_form_shown', True)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def about(request):
    """Renders the about page if the Sitelook object with ID 1
    has a value of True for 'show_about' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_about:
        about = About.objects.get(id=1)

        context = { 'about': about }

        response = render(request, 'site_pages/about.html', context)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def author_profile(request, profile_id):
    """Renders the author's profile page which will include up to 5 of their most
    recent public posts.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    profile_id (int): The PK of the AuthorProfile to be displayed.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    profile = AuthorProfile.objects.get(id=profile_id)
    posts = Post.objects.filter(author=profile, visibility='public').order_by('-date')
    posts = posts[:5]

    context = { 'profile': profile, 'posts': posts }

    context['show_subscribe_form'] = show_subscribe_form(request)

    response = render(request, 'site_pages/author_profile.html', context)
    response.set_cookie('subscribe_form_shown', True)

    return response


def timeline(request):
    """Renders the timeline page if the Sitelook object with ID 1
    has a value of True for 'show_timeline' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_timeline:
        years_qset = Post.objects.filter(visibility='public').dates('og_date', 'year')
        years = [ ]
        if len(years_qset) > 1:
            for i, date in enumerate(years_qset): # Limits to two years per dimension (row)
                if (i+1)%2 != 0:
                    row = [ date.year ]
                else:
                    row.append(date.year)
                    years.append(row)
        else: # If 1 year.
            row = [ years_qset[0].year ]
            years.append(row)

        context = {
            'months': MONTHS,
            'years': years,
        }

        response = render(request, 'site_pages/timeline.html', context)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def timeline_year(request, year):
    """Renders the timeline page for the specified year if the Sitelook object
    with ID 1 has a value of True for 'show_timeline' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    year (int): The year for which the timeline should be loaded.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_timeline:
        posts = Post.objects.filter(og_date__year=year, visibility='public')
        posts = posts.order_by('-og_date')

        context = {
            'pagetitle': 'Posts Originated in ' + str(year),
            'posts': posts
        }

        context['show_subscribe_form'] = show_subscribe_form(request)

        response = render(request, 'site_pages/timeline_timeperiod.html', context)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


def timeline_month(request, year, month):
    """Renders the timeline page for the specified year and month if the Sitelook object
    with ID 1 has a value of True for 'show_timeline' (configured in the
    administrative menu).

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    year (int): The year for which the timeline should be loaded.
    month (str): The month for which the timeline should be loaded.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    if sitelook.show_timeline:
        posts = Post.objects.filter(og_date__year=year, og_date__month=MONTHS_DICT[month.lower()], visibility='public')
        posts = posts.order_by('-og_date')
        pagetitle = 'Posts Originated in ' + month[:3] + ', ' + str(year)

        context = {
            'pagetitle': pagetitle,
            'posts': posts
        }

        response = render(request, 'site_pages/timeline_timeperiod.html', context)

        return response
    else:
        return HttpResponseRedirect(reverse('index'))


@staff_member_required
@otp_required
def admin_delete_thread(request, post_slug, thread_id):
    """Allows an admin (a user with superuser permission) to delete a Post's Thread
    if they have authenticated with OTP. Deleting a thread is a cascading operation
    which deletes all comments with the thread as a foreign key relationship.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_slug (str): The unique slug that identifies the Post to which the thread
    belongs and is used to redirect back to the correct post page.
    thread_id (int): The PK of the Thread to delete.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    t = Thread.objects.get(id=thread_id)
    t.delete()

    return HttpResponseRedirect(reverse('post', args=[post_slug, 'post-comments']))


@staff_member_required
@otp_required
def admin_delete_comment(request, post_slug, comment_id):
    """Allows an admin (a user with superuser permission) to delete a Post's Comment
    if they have authenticated with OTP.

    Parameters:
    request (WSGIRequest): A WSGIRequest object.
    post_slug (str): The unique slug that identifies the Post to which the thread
    belongs and is used to redirect back to the correct post page.
    comment_id (int): The PK of the Comment to delete.

    Returns
    HttpResponse: Directs the user to the appropriate template.
    """
    c = Comment.objects.get(id=comment_id)
    c.delete()

    return HttpResponseRedirect(reverse('post', args=[post_slug, 'post-comments']))