"""megacashforhomes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from acc import views
from django.urls import path , include
from acc.views import Blog_page, Blog_details
from django.conf import settings
from django.conf.urls.static import static
from acc.sitemaps import StaticViewSitemap, PostSitemap
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': StaticViewSitemap,
    'post': PostSitemap

}
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.home),
    url(r'^about/$', views.about, name="about"),
    url(r'^contact/$', views.contact, name="contact"),
    url(r'^meet/$', views.meet, name="meet"),
    url(r'^sell/$', views.sell, name="sell"),
    url(r'^pdf/$', views.pdf),
    path('blog/', Blog_page.as_view(), name="blog"),
    path('article/<int:pk>', Blog_details.as_view(), name="article"),
    path('sitemap.xml/', sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    url(r'^robots\.txt', include('robots.urls'))

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'acc.views.error_404_view'
