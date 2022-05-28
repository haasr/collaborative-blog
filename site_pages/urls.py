from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:post_slug>/', views.post, name='post'),
    path('post/<str:post_slug>/<str:goto_section>/', views.post, name='post'),

    path('post_comment_new_thread/<str:post_slug>',
        views.post_comment_new_thread, name='post_comment_new_thread'),

    path('post_comment_existing_thread/<str:post_slug>/<int:thread_id>/',
        views.post_comment_existing_thread, name='post_comment_existing_thread'),

    path('topics/', views.topics, name='topics'),
    path('topic_posts/<int:topic_id>/', views.topic_posts, name='topic_posts'),
    path('contact/', views.contact, name='contact'),
    path('contrib/', views.contrib, name='contrib'),
    path('about/', views.about, name='about'),
    path('author_profile/<int:profile_id>/', views.author_profile, name='author_profile'),
    path('timeline/', views.timeline, name='timeline'),
    path('timeline_year/<int:year>/', views.timeline_year, name='timeline_year'),
    path('timeline_month/<int:year>/<str:month>/', views.timeline_month, name='timeline_month'),

    path('admin_delete_thread/<str:post_slug>/<int:thread_id>/', views.admin_delete_thread, name='admin_delete_thread'),
    path('admin_delete_comment/<str:post_slug>/<int:comment_id>/', views.admin_delete_comment, name='admin_delete_comment'),
]