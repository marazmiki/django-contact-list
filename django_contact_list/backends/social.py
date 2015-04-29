# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.translation import ugettext_lazy as _
from django_contact_list.exceptions import InvalidAccountName
from django_contact_list.backends.base import Backend
import re
import urlparse


class SocialNetworkBackend(Backend):
    allowed_domains = []
    url = '{account}'
    no_follow = True

    def get_account_name(self, value):
        bits = urlparse.urlparse(value)

        if not bits.netloc:
            return bits.path

        regex = re.compile(self.get_regex_pattern(), re.U | re.I)
        match = regex.search(value)

        if match:
            return match.groupdict()['account']
        raise InvalidAccountName()

    def get_regex_pattern(self):
        bits = urlparse.urlparse(self.url)
        pattern = bits.path.replace('{account}', '(?P<account>.*?)')
        host = '|'.join([b.lstrip('www.') for b in self.get_allowed_domains()])
        host = 'https?://' + '(www\.)?(?P<host>' + host + ')' + pattern + '$'
        return host

    def get_allowed_domains(self):
        return list(set([b for b in self.allowed_domains +
                         [urlparse.urlparse(self.url).netloc]
                         if b is not None]))

    def get_link(self, value):
        return self.url.format(account=self.get_account_name(value))

    def get_text(self, value):
        return self.get_account_name(value)

    def validate(self, value):
        try:
            self.get_account_name(value)
        except InvalidAccountName:
            self.raise_error(_('Incorrect %s account name') % self.title)


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

    """
    title = _('Twitter')
    url = 'https://twitter.com/@{account}'

    def get_regex_pattern(self):
        return '^https?://(www\.)?twitter\.com/\@?(?P<account>.*?)$'


class YoutubeBackend(SocialNetworkBackend):
    title = _('YouTube')
    url = 'http://www.youtube.com/user/{account}'


class InstagramBackend(SocialNetworkBackend):
    title = _('Instagram')
    url = 'http://instagram.com/{account}'
