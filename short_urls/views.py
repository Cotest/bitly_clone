from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView
from django.views.generic.edit import CreateView

from .models import ShortUrl
from .forms import ShortUrlCreateForm


class ShortUrlCreateView(CreateView):

    model = ShortUrl
    form_class = ShortUrlCreateForm
    paginate_by = 1

    def form_valid(self, form):
        created = False
        if form.exist_short_slug:
            short_slug = form.exist_short_slug
        else:
            self.object = form.save()
            short_slug = self.object.short_slug
            created = True
        short_url = self.request.build_absolute_uri('/' + short_slug)
        if created:
            added_short_url = {
                'short_url': short_url,
                'url': self.object.url,
            }
            if self.request.session.get('short_urls'):
                self.request.session['short_urls'].append(added_short_url)
                self.request.session.modified = True
            else:
                self.request.session['short_urls'] = [added_short_url]
        context = self.get_context_data(form=form, short_url=short_url)
        return self.render_to_response(context)

    def get_short_urls(self):
        context = {}
        short_urls = self.request.session.get('short_urls')
        if not short_urls:
            return context
        paginator = Paginator(short_urls, self.paginate_by)
        page_num = self.request.GET.get('page')
        try:
            page_short_urls = paginator.page(page_num)
        except PageNotAnInteger:
            page_short_urls = paginator.page(1)
        except EmptyPage:
            page_short_urls = paginator.page(paginator.num_pages)
        context['page_short_urls'] = page_short_urls
        return context

    def get_context_data(self, **kwargs):
        kwargs.update(self.get_short_urls())
        return super(ShortUrlCreateView, self).get_context_data(**kwargs)


class ShortUrlRedirectView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        short_url = get_object_or_404(ShortUrl, short_slug=kwargs['short_slug'])
        return short_url.url
