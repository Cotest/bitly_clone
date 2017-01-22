from django.conf.urls import include
from django.conf.urls import url
from django.contrib import admin


urlpatterns = [
    url(r'^', include('short_urls.urls')),
    url(r'^admin/', admin.site.urls),
]
