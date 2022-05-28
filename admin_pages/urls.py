from django.urls import path, include
from . import views

app_name='admin_pages'

urlpatterns = [
    path('', views.admin_index, name='admin_index'),
    path('site_pages/manage_site_look/', views.manage_site_look, name='manage_site_look'),
    path('site_pages/manage_home/', views.manage_home, name='manage_home'),
    path('site_pages/manage_topics_header/', views.manage_topics_header, name='manage_topics_header'),
    path('site_pages/manage_about/', views.manage_about, name='manage_about'),
    path('site_pages/manage_contact/', views.manage_contact, name='manage_contact'),
    path('site_pages/manage_contrib/', views.manage_contrib, name='manage_contrib'),
    path('site_pages/manage_seo/', views.manage_seo, name='manage_seo'),

    path('manage_author_profile/<str:posts_redirect>', views.manage_author_profile, name='manage_author_profile'),
    path('manage_posts/', views.manage_posts, name='manage_posts'),
    path('new_post/', views.new_post, name='new_post'),
    path('edit_post/<int:post_id>/', views.edit_post, name='edit_post'),
    path('replace_post_image/<int:post_id>/', views.replace_post_image, name='replace_post_image'),
    path('confirm_delete_post/<int:post_id>/', views.confirm_delete_post, name='confirm_delete_post'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),

    path('manage_topics/', views.manage_topics, name='manage_topics'),
    path('edit_topic/<int:topic_id>/', views.edit_topic, name='edit_topic'),
    path('confirm_delete_topic/<int:topic_id>/', views.confirm_delete_topic, name='confirm_delete_topic'),
    path('delete_topic/<int:topic_id>/', views.delete_topic, name='delete_topic'),

    path('delete_post_topic/<int:post_id>/<int:topic_id>/', views.delete_post_topic, name='delete_post_topic'),
    path('add_topic/<int:post_id>/', views.add_topic, name='add_topic'),

    path('manage_post_collaborators/<int:post_id>/', views.manage_post_collaborators, name='manage_post_collaborators'),

    path('manage_users/', views.manage_users, name='manage_users'),
    path('toggle_superuser_status/<int:user_id>', views.toggle_superuser_status, name='toggle_superuser_status'),

    path('manage_email_account/', views.manage_email_account, name='manage_email_account'),
    path('manage_email_denylist/', views.manage_email_denylist, name='manage_email_denylist'),

    path('new_denylistemail/', views.new_denylistemail, name='new_denylistemail'),
    path('edit_denylistemail/<int:denylistemail_id>/', views.edit_denylistemail, name='edit_denylistemail'),
    path('delete_denylistemail/<int:denylistemail_id>/', views.delete_denylistemail, name='delete_denylistemail'),

    path('newsletter/manage_subscriber_newsletter/', views.manage_subscriber_newsletter, name='manage_subscriber_newsletter'),
    path('newsletter/manage_subscribers/', views.manage_subscribers, name='manage_subscribers'),

    path('newsletter/confirm_delete_subscriber/<str:subscriber_email>/', views.confirm_delete_subscriber, name='confirm_delete_subscriber'),
    path('newsletter/delete_subscriber/<str:subscriber_email>/', views.delete_subscriber, name='delete_subscriber'),

    path('forms/manage_viewer_contact_form/', views.manage_viewer_contact_form_settings, name='manage_viewer_contact_form_settings'),
    path('forms/manage_email_contact_form/', views.manage_email_contact_form_settings, name='manage_email_contact_form_settings'),
    path('forms/manage_contribute_form/', views.manage_contribute_form_settings, name='manage_contribute_form_settings'),
    path('forms/manage_subscribe_form/', views.manage_subscribe_form_settings, name='manage_subscribe_form_settings'),

    path('failures/mail_send_failures/', views.manage_mail_send_failures, name='manage_mail_send_failures'),
    path('failures/mail_send_failures/<int:days>/', views.manage_mail_send_failures, name='manage_mail_send_failures'),
    path('failures/mail_send_failures/delete_form_send_failure/<int:failure_id>/', views.delete_form_send_failure, name='delete_form_send_failure'),
    path('failures/mail_send_failures/delete_newsletter_send_failure/<int:failure_id>/', views.delete_newsletter_send_failure, name='delete_newsletter_send_failure'),
    path('failures/mail_send_failures/resend_form_email/', views.resend_form_email, name='resend_form_email'),
]