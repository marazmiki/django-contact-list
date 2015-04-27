# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import validate_email, URLValidator
from django.utils.translation import ugettext_lazy as _


class Backend(object):
    title = ''
    no_follow = False

    def raise_error(self, message):
        raise ValidationError({'__all__': message})

    def validate(self, value):
        pass

    def get_link(self, value):
        return reverse('go_away') + '?link=' + value

    def get_text(self, value):
        return value

    def get_html(self, value):
        link = self.get_link(value)
        text = self.get_text(value)
        if link is not None:
            return '<a href="{link}"{nofollow}>{text}</a>'.format(
                nofollow=' rel="nofollow"' if self.no_follow else '',
                link=link,
                text=text)
        return text


class PhoneBackend(Backend):
    title = _('Phone')

    def get_link(self, value):
        return 'tel:%s' % value

    def get_text(self, value):
        value = value.lstrip('+')
        return '+{country} ({defcode}) {one}-{two}-{three}'.format(
            country=value[0],
            defcode=value[1:4],
            one=value[4:7],
            two=value[7:9],
            three=value[9:]
        )

    def validate(self, value):
        if value[0] == '+':
            if value[1:].isdigit() and len(value) in [12]:
                return
        else:
            if not value.isdigit():
                self.raise_error(_('Phone number can only consist of numbers'))
            if len(value) not in [11]:
                self.raise_error('Wrong phone number')


class WebsiteBackend(Backend):
    title = _('Website')
    no_follow = True

    def validate(self, value):
        URLValidator()(value)

    def get_text(self, value):
        if value.lower().startswith('http://'):
            value = value[7:]
        if value.lower().startswith('https://'):
            value = value[8:]
        return value


class EmailBackend(Backend):
    title = _('E-mail')

    def validate(self, value):
        validate_email(value)

    def get_link(self, value):
        return 'mailto:%s' % value
