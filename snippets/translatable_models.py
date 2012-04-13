# !title: Translatable models for multilingual sites
# !date: 2012-04-13
# !tags: Django, Multilingual
# !author: Denis Veselov

# abstract model
from django.db import models
from django.utils.translation import get_language


class TranslatableModel(models.Model):

    class Meta:
        abstract = True

    def __getattr__(self, name):
        i18n_name = '%s_%s' % (name, get_language())
        attr = super(TranslatableModel, self).__getattribute__(i18n_name)
        if attr:
            return attr
        return super(TranslatableModel, self).__getattribute__('%s_ru' % name)


# use of TranslatableModel
from django.utils.translation import get_language, ugettext_lazy as _

from core.models import TranslatableModel


class ExampleModel(TranslatableModel):

    title_ru = models.CharField(_('title'), max_length=100)
    title_en = models.CharField(_('title'), max_length=100, blank=True)
    title_uk = models.CharField(_('title'), max_length=100, blank=True)
    image = models.ImageField(_('image'), upload_to='example_path')
    position = models.PositiveIntegerField(_('position'), default=100)

    def __unicode__(self):
        return self.title_ru
