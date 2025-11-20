from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AcademicsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        # ضع أسماء الـ URL patterns الرئيسية في academics/urls.py
        return ['academics:index', 'academics:subjects', 'academics:exams']

    def location(self, item):
        return reverse(item)
