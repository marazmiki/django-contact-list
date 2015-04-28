# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from rest_framework import test, status
from django_contact_list import settings, backends
from django_contact_list.models import Contact
from django_contact_list.utils import (get_available_backends, get_backend,
                                       get_type_choices)


User = get_user_model()


class SetUp(object):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user',
                                             email='user@example.com')
        self.client = test.APIClient()
        self.client.force_authenticate(self.user)


class SetUpObj(SetUp):
    def setUp(self):
        super(SetUpObj, self).setUp()
        self.contact = Contact.objects.create(user=self.user,
                                              account='marazmiki',
                                              type='vk')
        self.url = reverse('contacts_detail', kwargs={'pk': self.contact.pk})


class TestCreate(SetUp, test.APITestCase):
    def test_post_not_authentication(self):
        self.client.logout()
        resp = self.client.post(reverse('contacts_list_create'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)

    def test_post_bad_request(self):
        resp = self.client.post(reverse('contacts_list_create'), {})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)
        self.assertFalse(Contact.objects.exists())

    def test_post_good(self):
        resp = self.client.post(reverse('contacts_list_create'), {
            'type': 'facebook',
            'account': 'marazmiki'
        })
        self.assertEqual(status.HTTP_201_CREATED, resp.status_code)
        self.assertEqual(1, Contact.objects.count())
        self.assertEqual('facebook', Contact.objects.latest('pk').type)
        self.assertEqual('marazmiki', Contact.objects.latest('pk').account)


class TestList(SetUp, test.APITestCase):
    def test_get_not_authentication(self):
        self.client.logout()
        resp = self.client.get(reverse('contacts_list_create'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)

    def test_get_good(self):
        resp = self.client.get(reverse('contacts_list_create'))
        self.assertEqual(status.HTTP_200_OK, resp.status_code)

    def test_get_not_authenticated(self):
        self.client.logout()
        resp = self.client.get(reverse('contacts_list_create'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)


class TestUpdate(SetUpObj, test.APITestCase):
    def test_put_not_authentication(self):
        self.client.logout()
        resp = self.client.put(self.url, {'type': 'facebook'})
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)
        self.assertEqual('vk', Contact.objects.get(id=self.contact.pk).type)

    def test_put_authentication(self):
        resp = self.client.put(self.url, {'type': 'facebook',
                                          'account': 'marazmiki'})
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual('facebook', resp.data['type'])

    def test_patch(self):
        resp = self.client.patch(self.url, {'type': 'facebook'})
        self.assertEqual(status.HTTP_200_OK, resp.status_code)
        self.assertEqual('facebook', resp.data['type'])
        self.assertEqual('marazmiki', resp.data['account'])

    def test_put_bad_request(self):
        resp = self.client.put(self.url, {'type': 'not_exist',
                                          'account': ''})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, resp.status_code)


class TestDelete(SetUpObj, test.APITestCase):
    def test_delete_not_authentication(self):
        self.client.logout()
        resp = self.client.delete(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)
        self.assertEqual(1, Contact.objects.count())

    def test_delete_authentication(self):
        resp = self.client.delete(self.url)
        self.assertEqual(status.HTTP_204_NO_CONTENT, resp.status_code)
        self.assertFalse(Contact.objects.exists())


class TestGetAvailableBackends(test.APITestCase):
    def test_default(self):
        self.skipTest('')
        self.assertEqual(settings.BACKENDS, get_available_backends())

    def test_patched(self):
        self.skipTest('')
        back = settings.BACKENDS
        settings.BACKENDS = [1, 2, 3]
        self.assertEqual([1, 2, 3], get_available_backends())
        settings.BACKENDS = back


class TestGetBackend(test.APITestCase):
    def test_1(self):
        print(get_backend('vk'))

    def test_(self):
        print(get_type_choices())

#
[
    'Backend', 'EmailBackend', 'WebsiteBackend',
    'FacebookBackend', 'VkontakteBackend', 'DirtyBackend', 'GooglePlusBackend',
    'HabrahabrBackend', 'LeprosoriumBackend', 'MoiMirBackend',
    'OdnoklassnikiBackend', 'TwitterBackend', 'YoutubeBackend',
    'InstagramBackend'
]


class TestWebsiteBackend(test.APITestCase):
    def test_validate(self):
        backends.WebsiteBackend().validate('http://example.com')

    def test_validate_fails(self):
        with self.assertRaises(ValidationError):
            backends.WebsiteBackend().validate('not-a-site')

    def test_get_text_http(self):
        self.assertEqual('1.com',
                         backends.WebsiteBackend().get_text('http://1.com'))

    def test_get_text_https(self):
        self.assertEqual('1.com',
                         backends.WebsiteBackend().get_text('https://1.com'))

    def test_nofollow(self):
        self.assertIn('nofollow',
                      backends.WebsiteBackend().get_html('https://1.com'))


class TestPhoneBackend(test.APITestCase):
    def test_get_link(self):
        self.assertEqual('tel:+79051234567',
                         backends.PhoneBackend().get_link('+79051234567'))

    def test_get_text(self):
        self.assertEqual('+7 (905) 123-45-67',
                         backends.PhoneBackend().get_text('+79051234567'))

    def test_validate_iso(self):
        self.assertIsNone(backends.PhoneBackend().validate('+79051234567'))

    def test_validate_digits(self):
        self.assertIsNone(backends.PhoneBackend().validate('+7905abcdefg'))

    def test_validate_digits_not_startwith_plus(self):
        with self.assertRaises(ValidationError):
            self.assertIsNone(backends.PhoneBackend().validate('9051234567'))

    def test_validate_no_digits_not_startwith_plus(self):
        with self.assertRaises(ValidationError):
            self.assertIsNone(backends.PhoneBackend().validate('905abcdefg'))

    def test_validate_digits__short(self):
        with self.assertRaises(ValidationError):
            self.assertIsNone(backends.PhoneBackend().validate('123456'))

    def test_validate_digits_without_plus_correct(self):
        self.assertIsNone(backends.PhoneBackend().validate('79051234567'))

    def test_text(self):
        self.assertEqual('<a href="tel:+79051234567">+7 (905) 123-45-67</a>',
                         backends.PhoneBackend().get_html('+79051234567'))

    def test_nofollow(self):
        self.assertNotIn('nofollow',
                         backends.PhoneBackend().get_html('+79051234567'))


class TestICQBackend(test.APITestCase):
    def test_validate_non_digit(self):
        with self.assertRaises(ValidationError):
            backends.ICQBackend().validate('non-digit')

    def test_validate_ok(self):
        self.assertIsNone(backends.ICQBackend().validate('1245678'))

    def test_validate_too_short(self):
        with self.assertRaises(ValidationError):
            backends.ICQBackend().validate('1234')

    def test_validate__too_long(self):
        with self.assertRaises(ValidationError):
            backends.ICQBackend().validate('1234567890')

    def test_link(self):
        self.assertEqual('https://icq.com/people/123456',
                         backends.ICQBackend().get_link('123456'))


class TestSkypeBackend(test.APITestCase):
    def test_link(self):
        self.assertEqual('skype:batman',
                         backends.SkypeBackend().get_link('batman'))


class TestJabberBackend(test.APITestCase):
    def test_link(self):
        self.assertEqual('xmpp:serg@google.com',
                         backends.JabberBackend().get_link('serg@google.com'))
