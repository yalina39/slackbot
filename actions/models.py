from django.db import models

class Message(models.Model):
    channel = models.CharField(max_length=15)
    user = models.CharField(max_length=15)
    text = models.TextField()
    pattern = models.CharField(max_length=10)

