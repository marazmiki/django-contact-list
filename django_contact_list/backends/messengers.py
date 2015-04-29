# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.translation import ugettext_lazy as _
from django_contact_list.backends.base import Backend, EmailBackend


class JabberBackend(EmailBackend):
    """
    >>> backend = JabberBackend()
    >>> str(backend.get_link('admin@example.com'))
    'xmpp:admin@example.com'

    >>> str(backend.get_html('admin@example.com'))
    '<a href="xmpp:admin@example.com">admin@example.com</a>'

    >>> assert 'nofollow' not in backend.get_html('admin@example.com')

    """
    title = _('Jabber ID')

    def get_link(self, value):
        return 'xmpp:%s' % value


class ICQBackend(Backend):
    """
    >>> backend = ICQBackend()
    >>> str(backend.get_link('123456'))
    'https://icq.com/people/123456'

    >>> backend.validate('1245678')

    >>> backend.validate('1234')
    Traceback (most recent call last):
      ...
    ValidationError: {u'__all__': [u'ICQ number can be from 5 to 9 chars in length']}

    >>> backend.validate('1234567890')
    Traceback (most recent call last):
      ...
    ValidationError: {u'__all__': [u'ICQ number can be from 5 to 9 chars in length']}

    >>> backend.validate('non-digit')
    Traceback (most recent call last):
      ...
    ValidationError: {u'__all__': [u'ICQ number can only consist of numbers']}

    >>> str(backend.get_link('123456'))
    'https://icq.com/people/123456'
    """
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
    """
    >>> backend = SkypeBackend()

    >>> str(backend.get_link('batman'))
    'skype:batman'

    """
    title = _('Skype')

    def get_link(self, value):
        return 'skype:%s' % value
