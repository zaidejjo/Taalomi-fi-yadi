from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AIChatSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['chat:home']

    def location(self, item):
        return reverse(item)
