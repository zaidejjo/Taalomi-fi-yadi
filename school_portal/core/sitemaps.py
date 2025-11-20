from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class CoreSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return ['core:home']  # الاسم مطابق للـ view الرئيسية

    def location(self, item):
        return reverse(item)
