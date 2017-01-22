import string
import random

from django.conf import settings
from django.db import models


class ShortUrl(models.Model):

    short_slug = models.SlugField(
        'Короткий URL',
        max_length=settings.LENGTH_SHORT_SLUG,
        primary_key=True
    )
    url = models.URLField('URL', max_length=255)
    create_date = models.DateField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Короткий URL'
        verbose_name_plural = 'Короткие URL'

    def get_absolute_url(self):
        return self.url

    def __str__(self):
        return self.short_slug

    @classmethod
    def is_unique_short_slug(cls, short_slug):
        return not cls.objects.filter(short_slug=short_slug).exists()

    @classmethod
    def generate_short_slug(cls, url):
        length = settings.LENGTH_SHORT_SLUG
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        while True:
            short_slug = ''.join(random.choice(chars) for x in range(length))
            try:
                exist_url = cls.objects.get(short_slug=short_slug)
            except cls.DoesNotExist:
                return short_slug

    @classmethod
    def get_short_slug_by_url(cls, url):
        try:
            exist_url = cls.objects.get(url=url)
        except cls.DoesNotExist:
            return None
        except cls.MultipleObjectsReturned:
            return cls.objects.filter(url=url).first().short_slug
        return exist_url.short_slug
