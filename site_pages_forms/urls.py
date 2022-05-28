from django.urls import path
from . import views

urlpatterns = [
    path('submit_subscribe_form/', views.submit_subscribe_form,
        name='submit_subscribe_form'),

    path('submit_contact_email/', views.submit_contact_email,
        name='submit_contact_email'),

    path('submit_contact_form/', views.sumbit_contact_form,
        name='submit_contact_form'),

    path('submit_contrib_form/', views.submit_contrib_form,
        name='submit_contrib_form'),
]