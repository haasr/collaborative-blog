from django.urls import path
from . import views

urlpatterns = [
    path('unsubscribe/<str:email>', views.unsubscribe, name='unsubscribe'),
]