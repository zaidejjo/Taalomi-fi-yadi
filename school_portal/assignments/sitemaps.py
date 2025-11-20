from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AssignmentsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return ['assignments:assignment_list']

    def location(self, item):
        return reverse(item)
