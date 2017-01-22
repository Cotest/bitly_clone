from django import forms

from .models import ShortUrl


class ShortUrlCreateForm(forms.ModelForm):

    short_slug = forms.SlugField(required=False)

    exist_short_slug = ''

    class Meta:
        model = ShortUrl
        fields = ('url', 'short_slug')

    def clean_short_slug(self):
        short_slug = self.cleaned_data.get('short_slug', '')
        url = self.cleaned_data['url']
        if not short_slug:
            exist_short_slug = ShortUrl.get_short_slug_by_url(url)
            if exist_short_slug:
                self.exist_short_slug = exist_short_slug
                return ''
            return ShortUrl.generate_short_slug(url)
        if ShortUrl.is_unique_short_slug(short_slug):
            return short_slug
        elif ShortUrl.objects.filter(url=url, short_slug=short_slug).exists():
            self.exist_short_slug = short_slug
            return ''
        raise forms.ValidationError('Выбранное вами сокращение URL уже занято.')