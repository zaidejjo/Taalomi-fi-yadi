from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AttendanceSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ['attendance:absence_list']

    def location(self, item):
        return reverse(item)
