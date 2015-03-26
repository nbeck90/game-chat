from django.db import models
from django.core.urlresolvers import reverse


class Article(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateField()

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.pk})


class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField()