from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import datetime, date


# Create your models here.


class Testimonial(models.Model):
    name = models.CharField(max_length=100, null=True)
    review = models.TextField(null=True)
    id = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.name


class Customer(models.Model):
    name = models.CharField(max_length=100, null=True)
    price = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=500, null=True)
    mail = models.CharField(max_length=100, null=True)
    condition = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    title_2 = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body_1 = models.TextField(default="")
    body_2 = models.TextField(default="")
    body_3 = models.TextField(default="")
    body_4 = models.TextField(default="")
    post_date = models.DateField(auto_now_add=True)
    image = models.ImageField(null=False, blank=True, upload_to='images/')

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return f'/{self.title}/'