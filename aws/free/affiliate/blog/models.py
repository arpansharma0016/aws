from django.db import models

class Blog(models.Model):
    post = models.TextField()
    name = models.TextField()
    image = models.TextField()

    def __str__(self):
        return self.name
    
class Comments(models.Model):
    comment = models.TextField()
    email = models.TextField()
    name = models.TextField()
    post_id = models.IntegerField()
