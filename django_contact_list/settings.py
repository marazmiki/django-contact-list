# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.translation import ugettext_lazy as _
from django.conf import settings


BACKENDS = getattr(settings, 'CONTACTS_BACKENDS', (
    (_('Basic'), (
        ('email', 'django_contact_list.backends.EmailBackend'),
        ('website', 'django_contact_list.backends.WebsiteBackend'),
        ('phone', 'django_contact_list.backends.PhoneBackend'),
    )),
    (_('Messengers'), (
        ('jabber', 'django_contact_list.backends.JabberBackend'),
        ('icq', 'django_contact_list.backends.ICQBackend'),
        ('skype', 'django_contact_list.backends.SkypeBackend'),
    )),
    (_('Social networks'), (
        ('vk', 'django_contact_list.backends.VkontakteBackend'),
        ('facebook', 'django_contact_list.backends.FacebookBackend'),
        ('habrahabr', 'django_contact_list.backends.HabrahabrBackend'),
        ('dirty', 'django_contact_list.backends.DirtyBackend'),
        ('moimir', 'django_contact_list.backends.MoiMirBackend'),
        ('leprosorium', 'django_contact_list.backends.LeprosoriumBackend'),
        ('odnoklassniki', 'django_contact_list.backends.OdnoklassnikiBackend'),
        ('googleplus', 'django_contact_list.backends.GooglePlusBackend'),
        ('twitter', 'django_contact_list.backends.TwitterBackend'),
        ('youtube', 'django_contact_list.backends.YoutubeBackend'),
        ('instagram', 'django_contact_list.backends.InstagramBackend'),
    )),
))
