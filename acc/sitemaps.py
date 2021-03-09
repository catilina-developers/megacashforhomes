from django.contrib.sitemaps import Sitemap
from .models import Post
from django.shortcuts import reverse


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ['about', 'contact', 'sell', 'blog', 'meet', ]

    def location(self, item):
        return reverse(item)

class PostSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Post.objects.all()
