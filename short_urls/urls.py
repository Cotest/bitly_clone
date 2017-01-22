from django.conf.urls import url
from django.conf import settings

from .views import ShortUrlCreateView
from .views import ShortUrlRedirectView


urlpatterns = [
    url(r'^$', ShortUrlCreateView.as_view(), name='short_url_create'),
    url(
        r'^(?P<short_slug>\w{1,%d})$' % settings.LENGTH_SHORT_SLUG,
        ShortUrlRedirectView.as_view(),
        name='redirect_url_view'
    ),
]
