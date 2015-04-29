# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.core.exceptions import ValidationError
from django.core.validators import validate_email, URLValidator
from django.utils.translation import ugettext_lazy as _


class Backend(object):
    """

    >>> backend = Backend()
    >>> backend.validate("Test")

    """
    title = ''
    no_follow = False

    def raise_error(self, message):
        raise ValidationError({'__all__': message})

    def validate(self, value):
        """
        >>> backend = Backend()
        >>> backend.validate('Some value')
        >>>
        """

    def get_link(self, value):
        """
        >>> backend = Backend()
        >>> str(backend.get_link('Just a link'))
        'Just a link'
        """
        return value

    def get_text(self, value):
        """
        >>> backend = Backend()
        >>> str(backend.get_text('Just a text'))
        'Just a text'
        """
        return value

    def get_html(self, value):
        """
        >>> backend = Backend()

        >>> str(backend.get_html('Text'))
        '<a href="Text">Text</a>'

        >>> backend.no_follow = True
        >>> str(backend.get_html('Text'))
        '<a href="Text" rel="nofollow">Text</a>'


        >>> backend.get_link = lambda value: None
        >>> str(backend.get_html('Text'))
        'Text'

        """
        link = self.get_link(value)
        text = self.get_text(value)
        if link is not None:
            return '<a href="{link}"{nofollow}>{text}</a>'.format(
                nofollow=' rel="nofollow"' if self.no_follow else '',
                link=link,
                text=text)
        return text


class PhoneBackend(Backend):
    """
    >>> backend = PhoneBackend()

    >>> str(backend.get_link('+79051234567'))
    'tel:+79051234567'

    >>> backend.validate('79051234567')
    >>>

    >>> str(backend.get_html('+79051234567'))
    '<a href="tel:+79051234567">+7 (905) 123-45-67</a>'

    >>> assert 'nofollow' not in backend.get_html('+79051234567')

    >>> str(backend.get_text('+79051234567'))
    '+7 (905) 123-45-67'

    >>> backend.validate('+79051234567')

    >>> backend.validate('+7905abcdefg')

    >>> backend.validate('9051234567')
    Traceback (most recent call last):
      ...
    ValidationError: ...

    >>> backend.validate('905abcdefg')
    Traceback (most recent call last):
      ...
    ValidationError: ...

    >>> backend.validate('123456')
    Traceback (most recent call last):
      ...
    ValidationError: ...
    """

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
    """
    >>> backend = WebsiteBackend()


    >>> backend.validate('http://example.com')
    >>>

    >>> backend.validate('not-a-site')
    Traceback (most recent call last):
      ...
    ValidationError: ...

    >>> str(backend.get_text('http://1.com'))
    '1.com'

    >>> str(backend.get_text('https://1.com'))
    '1.com'

    >>> assert 'nofollow' in backend.get_html('https://1.com')

    """
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
        """
        >>> backend = EmailBackend()

        >>> backend.validate('admin@example.com')

        >>> backend.validate('not-a-email')
        Traceback (most recent call last):
          ...
        ValidationError: ...

        >>> str(backend.get_html('admin@example.com'))
        '<a href="mailto:admin@example.com">admin@example.com</a>'

        """
        validate_email(value)

    def get_link(self, value):
        return 'mailto:%s' % value
