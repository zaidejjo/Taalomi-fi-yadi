from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AIChatSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['chat_home', 'chat_ai']  # أسماء الـ views فقط

    def location(self, item):
        return reverse(f'ai_chat:{item}')  # استخدام namespace
