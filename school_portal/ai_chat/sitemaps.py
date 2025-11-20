from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class AIChatSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return ['chat_home']  # الاسم مطابق للـ URL في ai_chat/urls.py

    def location(self, item):
        return reverse(f'ai_chat:{item}')  # namespace صحيح
