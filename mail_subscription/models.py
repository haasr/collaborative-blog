from django.db import models

class EmailSubscriber(models.Model):
    email_addr = models.CharField(max_length=320, blank=False, null=False)
    first_name = models.CharField(max_length=75)
    last_name = models.CharField(max_length=75)
    subscribed_at = models.DateTimeField(auto_now_add=True)