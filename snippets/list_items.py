# !title: ListItem base model and admin
# !date: 2012-07-10
# !tags: Django
# !author: Dima Kukushkin

# models.py

from django.db import models
from django.db.models.query import QuerySet
from django.utils.translation import ugettext_lazy as _


class ListitemQuerySet(QuerySet):

    def active(self):
        return self.filter(is_active=True)


class ListItemManager(models.Manager):

    def get_query_set(self):
        return ListitemQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_query_set().active()


class ListItem(models.Model):

    is_active = models.BooleanField(_(u'is active'), default=True)
    weight = models.PositiveIntegerField(_(u'weight'), db_index=True,
                                         default=0)
    objects = ListItemManager()

    class Meta:
        ordering = ['weight']
        abstract = True


# admin.py

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class ListItemAdmin(admin.ModelAdmin):

    list_display = ['is_active', 'weight']
    list_editable = ['weight']
    list_filter = ['is_active']
    actions = ['activate', 'deactivate']
    fieldsets = (
        (_('View parameters'), {
            'classes': ('collapse', 'wide'),
            'fields': ('is_active', 'weight')
        }),
    )

    def activate(self, request, qs):
        qs.update(is_active=True)
    activate.short_description = _(
        u'Activate selected %(verbose_name_plural)s'
    )

    def deactivate(self, request, qs):
        qs.update(is_active=False)
    deactivate.short_description = _(
        u'Deactivate selected %(verbose_name_plural)s'
    )
