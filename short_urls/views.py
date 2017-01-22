from django.views.generic.edit import CreateView
from django.views.generic.base import RedirectView
from django.shortcuts import get_object_or_404

from .models import ShortUrl
from .forms import ShortUrlCreateForm


class ShortUrlCreateView(CreateView):

    model = ShortUrl
    form_class = ShortUrlCreateForm

    def form_valid(self, form):
        if form.exist_short_slug:
            short_slug = form.exist_short_slug
        else:
            self.object = form.save()
            short_slug = self.object.short_slug
        short_url = self.request.build_absolute_uri('/' + short_slug)
        context = self.get_context_data(form=form, short_url=short_url)
        return self.render_to_response(context)


class ShortUrlRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = get_object_or_404(ShortUrl, short_slug=kwargs['short_slug'])
        return short_url.url
