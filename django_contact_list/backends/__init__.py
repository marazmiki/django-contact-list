# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django_contact_list.backends.base import (
    Backend, PhoneBackend, EmailBackend, WebsiteBackend)
from django_contact_list.backends.messengers import (
    SkypeBackend, ICQBackend, JabberBackend)
from django_contact_list.backends.social import (
    FacebookBackend, VkontakteBackend, DirtyBackend, GooglePlusBackend,
    HabrahabrBackend, LeprosoriumBackend, MoiMirBackend, OdnoklassnikiBackend,
    TwitterBackend, YoutubeBackend, InstagramBackend
)

__all__ = [
    'Backend', 'PhoneBackend', 'EmailBackend', 'WebsiteBackend',
    'SkypeBackend', 'ICQBackend', 'JabberBackend',
    'FacebookBackend', 'VkontakteBackend', 'DirtyBackend', 'GooglePlusBackend',
    'HabrahabrBackend', 'LeprosoriumBackend', 'MoiMirBackend',
    'OdnoklassnikiBackend', 'TwitterBackend', 'YoutubeBackend',
    'InstagramBackend'
]
