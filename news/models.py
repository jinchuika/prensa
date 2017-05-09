from django.db import models
from datetime import datetime


class NewsSource(models.Model):
    feed_url = models.URLField()
    name = models.CharField(max_length=128)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "News Source"
        verbose_name_plural = "News Sources"

    def __str__(self):
        return self.name


class Article(models.Model):
    link = models.URLField(unique=True)
    title = models.TextField()
    summary = models.TextField(null=True)
    parsed = models.DateTimeField(default=datetime.now())
    published = models.DateTimeField()
    enclosure = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title[:25]
