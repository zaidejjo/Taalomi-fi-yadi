from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AcademicsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # كل الـ URLs الرئيسية في التطبيق
        return ['academics:index', 'academics:subjects', 'academics:exams']

    def location(self, item):
        return reverse(item)
