from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question

class ChatHistory(models.Model):
    message = models.TextField()
    sender = models.CharField(max_length=10)  # 'user' أو 'ai'
    timestamp = models.DateTimeField(auto_now_add=True)
