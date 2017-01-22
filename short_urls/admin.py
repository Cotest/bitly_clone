from django.contrib import admin

from .models import ShortUrl


class ShortUrlAdmin(admin.ModelAdmin):
    list_display = ['short_slug', 'url', 'create_date']
    fields = ['url', 'short_slug', 'create_date']
    readonly_fields = ['create_date']

admin.site.register(ShortUrl, ShortUrlAdmin)
