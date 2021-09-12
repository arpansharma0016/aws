from django.db import models

class Newsletter(models.Model):
    email = models.TextField()
