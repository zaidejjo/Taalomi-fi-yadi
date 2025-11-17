from django.db import models

class Competition(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField(blank=True)
    deadline = models.DateField()
    apply_link = models.URLField(blank=True)
