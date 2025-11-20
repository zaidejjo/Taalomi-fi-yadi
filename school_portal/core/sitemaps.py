from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class CoreSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # ضع أسماء URL patterns الرئيسية في core/urls.py
        return ['core:home']  # غيّر 'home' باسم view الرئيسية

    def location(self, item):
        return reverse(item)
