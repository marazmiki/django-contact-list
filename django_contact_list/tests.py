# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import test, status
from django_contact_list.admin import ContactAdmin    # NOQA
from django_contact_list import settings, backends
from django_contact_list.backends import social, base, messengers
from django_contact_list.models import Contact
from django_contact_list.utils import (get_available_backends, get_backend,
                                       get_type_choices)
import doctest


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
    def test_get_backend(self):
        self.assertEqual(backends.VkontakteBackend, get_backend('vk'))

    def test_(self):
        self.skipTest('not implemented yet')
        print(get_type_choices())

#
[
    'Backend', 'EmailBackend',
    'FacebookBackend', 'VkontakteBackend', 'DirtyBackend', 'GooglePlusBackend',
    'HabrahabrBackend', 'LeprosoriumBackend', 'MoiMirBackend',
    'OdnoklassnikiBackend', 'TwitterBackend', 'YoutubeBackend',
    'InstagramBackend'
]


def load_tests(loader, tests, ignore):
    tests.addTests([
        doctest.DocTestSuite(social, optionflags=doctest.ELLIPSIS),
        doctest.DocTestSuite(base, optionflags=doctest.ELLIPSIS),
        doctest.DocTestSuite(messengers, optionflags=doctest.ELLIPSIS)
    ])
    return tests
