# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.translation import ugettext_lazy as _
from django_contact_list.backends.base import Backend, EmailBackend


class JabberBackend(EmailBackend):
    title = _('Jabber ID')

    def get_link(self, value):
        return 'xmpp:%s' % value


class ICQBackend(Backend):
    title = _('ICQ')

    def validate(self, value):
        if not value.isdigit():
            self.raise_error(
                _('ICQ number can only consist of numbers')
            )
        if len(value) < 5 or len(value) > 9:
            self.raise_error(
                _('ICQ number can be from 5 to 9 chars in length')
            )

    def get_link(self, value):
        return 'https://icq.com/people/%s' % value


class SkypeBackend(Backend):
    title = _('Skype')

    def get_link(self, value):
        return 'skype:%s' % value
