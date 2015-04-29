# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.translation import ugettext_lazy as _
from django.utils import six
from django_contact_list.exceptions import InvalidAccountName
from django_contact_list.backends.base import Backend
import re


urlparse = six.moves.urllib.parse.urlparse


class SocialNetworkBackend(Backend):
    allowed_domains = []
    url = '{account}'
    no_follow = True
    account_re = '.*?'

    def get_account_name(self, value):
        bits = urlparse(value)

        if not bits.netloc:
            return bits.path

        if bits.netloc.lower() not in self.allowed_domains:
            raise InvalidAccountName()

        regex = re.compile(self.get_regex_pattern(), re.U | re.I)
        match = regex.search(value)

        if match:
            return match.groupdict()['account']
        raise InvalidAccountName()

    def get_regex_pattern(self):
        bits = urlparse(self.url)
        pattern = bits.path.replace('{account}', '(?P<account>.*?)')
        host = '|'.join([b.lstrip('www.') for b in self.get_allowed_domains()])
        host = 'https?://' + '(www\.)?(?P<host>' + host + ')' + pattern + '$'
        return host

    def get_allowed_domains(self):
        return list(set([b for b in self.allowed_domains +
                         [urlparse(self.url).netloc]
                         if b is not None]))

    def get_link(self, value):
        return self.url.format(account=self.get_account_name(value))

    def get_text(self, value):
        return self.get_account_name(value)

    def validate(self, value):
        try:
            self.get_account_name(value)
        except InvalidAccountName:
            self.raise_error(_('Incorrect %s account name: %s') % (self.title, value))


class VkontakteBackend(SocialNetworkBackend):
    title = _('V Kontakte')
    allowed_domains = ['vk.com', 'm.vk.com', 'vkontakte.ru', 'm.vkontakte.ru']
    url = 'https://vk.com/{account}'


class HabrahabrBackend(SocialNetworkBackend):
    title = _('Habrahabr')
    allowed_domains = ['habrahabr.ru', 'habr.ru']
    url = 'https://habrahabr.ru/users/{account}'


class FacebookBackend(SocialNetworkBackend):
    title = _('Facebook')
    url = 'https://facebook.com/{account}'


class DirtyBackend(SocialNetworkBackend):
    title = _('Dirty.ru')
    url = 'http://d3.ru/user/{account}'


class MoiMirBackend(SocialNetworkBackend):
    title = _('Moi Mir @ Mail.ru')
    url = 'http://my.mail.ru/mail/{account}/'


class LeprosoriumBackend(SocialNetworkBackend):
    title = _('Leprosorium')
    url = 'https://leprosorium.ru/users/{account}'


class OdnoklassnikiBackend(SocialNetworkBackend):
    title = _('Odnoklassniki')
    url = 'http://www.odnoklassniki.ru/profile/{account}/about'


class GooglePlusBackend(SocialNetworkBackend):
    title = _('Google Plus')
    url = 'https://plus.google.com/u/0/{account}/posts'


class TwitterBackend(SocialNetworkBackend):
    """

    >>> backend = TwitterBackend()

    >>> str(backend.get_link('marazmiki'))
    'https://twitter.com/@marazmiki'

    >>> str(backend.get_html('marazmiki'))
    '<a href="https://twitter.com/@marazmiki" rel="nofollow">marazmiki</a>'

    >>> backend.validate('marazmiki')

    >>> backend.validate('http://twitter.com/marazmiki')

    >>> backend.validate('http://twitter.com/@marazmiki')

    >>> backend.validate('https://twitter.com/marazmiki')

    >>> backend.validate('https://twitter.com/@marazmiki')

    >>> backend.validate('http://vk.com/durov')
    Traceback (most recent call last): 
      ... 
    ValidationError: ...

    """
    account_re = '^@?(\w+)$'
    title = _('Twitter')
    url = 'https://twitter.com/@{account}'
    allowed_domains = ['twitter.com', 'www.twitter.com']

    def validate(self, value):
        bits = urlparse(value)

        if bits.netloc and bits.netloc.lower() not in self.allowed_domains:
            self.raise_error('Wrong domain')


        if not bits.netloc:
            if not re.compile(self.account_re).search(bits.path.strip('/')):
                self.raise_error('wrong account name')


        regex = re.compile(r'^https?://(www\.)?.twitter\.com/\@?(\w+)/?$', re.I | re.U)
        if not regex.search(value):
            self.raise_error('Wrong: %s' % value)

    def get_regex_pattern(self):
        return '^https?://(www\.)?twitter\.com/\@?(?P<account>[a-zA-Z0-9_]*+)$'


class YoutubeBackend(SocialNetworkBackend):
    title = _('YouTube')
    url = 'http://www.youtube.com/user/{account}'


class InstagramBackend(SocialNetworkBackend):
    title = _('Instagram')
    url = 'http://instagram.com/{account}'
