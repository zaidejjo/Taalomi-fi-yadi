from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class CompetitionsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return ['competitions:competition_list']

    def location(self, item):
        return reverse(item)
