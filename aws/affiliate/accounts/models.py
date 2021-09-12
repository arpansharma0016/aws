from django.db import models


class Product(models.Model):
    
    username = models.TextField()
    product_image = models.TextField()
    product_name = models.TextField()
    product_text_link = models.TextField()
    product_description = models.TextField()
    product_price = models.DecimalField(null=True,decimal_places=2,max_digits=1000)
    product_category = models.TextField(blank=True)

    
class Visitor_counter(models.Model):
    
    counter = models.IntegerField(default=0)
    username = models.TextField()
    
class Info(models.Model):
    
    username = models.TextField()
    currency = models.TextField()
    website_name = models.TextField()
    website_title = models.TextField()
    facebook = models.TextField()
    instagram = models.TextField()
    twitter = models.TextField()
    country = models.TextField()
    payment_id = models.TextField(null=True)
    order_id = models.TextField(null=True)
    kind_of_products = models.TextField()
    day_of_subscription = models.TextField(blank=True,null=True)
    day_of_expiry = models.TextField(blank=True,null=True)
    month_of_subscription = models.TextField(blank=True,null=True)
    month_of_expiry = models.TextField(blank=True,null=True)
    year_of_subscription = models.TextField(blank=True,null=True)
    year_of_expiry = models.TextField(blank=True,null=True)
    paid = models.BooleanField(default=False)
    on_trial = models.BooleanField(default=True)
    trial_done = models.BooleanField(default=False)
    trial_start = models.TextField(blank=True,null=True)
    trial_end = models.TextField(blank=True,null=True)
    trial = models.BooleanField(default=False)
    
 

class Confirm(models.Model):
    username = models.TextField()
    name = models.TextField()
    email = models.TextField()
    password = models.TextField()
    otp = models.TextField()
    attempts = models.IntegerField(default=0)

class Password(models.Model):
    username = models.TextField()
    otp = models.TextField()
    confirmed = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)


class Banner(models.Model):
    username = models.TextField()
    banner_category = models.TextField()
    banner_link = models.TextField()


class Widget(models.Model):
    username = models.TextField()
    widget_category = models.TextField()
    widget_link = models.TextField()

class Tag(models.Model):
    username = models.TextField()
    tag = models.TextField()

