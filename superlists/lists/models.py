from django.db import models
from django.shortcuts import resolve_url


class List(models.Model):

    def get_absolute_url(self):
        return resolve_url('view_list', self.pk)


class Item(models.Model):
    text = models.TextField()
    list = models.ForeignKey(List)

    class Meta:
        ordering = ('pk',)
        unique_together = ('list', 'text')

    def __str__(self):
        return self.text

    def save(self, *args, **kwargs):
        self.full_clean()
        #super().save(*args, **kwargs)
        super(Item, self).save(*args, **kwargs)
