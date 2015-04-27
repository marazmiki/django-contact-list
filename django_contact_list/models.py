# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf import settings as django_settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django_contact_list.utils import get_backend, get_type_choices


@python_2_unicode_compatible
class Contact(models.Model):
    user = models.ForeignKey(django_settings.AUTH_USER_MODEL,
                             related_name='contacts', verbose_name=_('user'))
    type = models.CharField(_('account type'), max_length=255,
                            default='', choices=get_type_choices())
    account = models.CharField(_('account'), max_length=255,
                               default='')

    @property
    def backend(self):
        return get_backend(self.type)()

    def link(self):
        return self.backend.get_link(self.account)

    def text(self):
        return self.backend.get_text(self.account)

    def html(self):
        return self.backend.get_html(self.account)

    def clean(self):
        self.backend.validate(self.account)

    def __str__(self):
        return self.link()

    class Meta(object):
        verbose_name = _('contact')
        verbose_name_plural = _('contacts')
        ordering = ['user', 'pk']
