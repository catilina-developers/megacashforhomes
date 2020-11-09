from django.db import models
from django.utils import timezone

# Create your models here.
class Blog(models.Model):
    heading_1 = models.TextField(null=True)
    heading_2 = models.TextField(null=True)
    content_1 = models.TextField(null=True)
    content_2 = models.TextField(null=True)
    content_3 = models.TextField(null=True)
    content_4 = models.TextField(null=True)
    id = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return self.heading_1


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

class Users_ip(models.Model):
    user_ip = models.CharField(max_length=30, null=True)
    visit_time = models.DateTimeField(default=timezone.now)
    