from __future__ import absolute_import

from datetime import datetime
from datetime import timedelta

from celery import shared_task

from .models import ShortUrl


@shared_task
def clear_old_short_url():
    last_day = datetime.now() - timedelta(days=30)
    ShortUrl.objects.filter(create_date__lte=last_day).delete()