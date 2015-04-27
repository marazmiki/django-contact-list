# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from rest_framework import test, status
from django_contact_list.models import Contact
from django_contact_list.utils import get_available_backends, get_backend, get_type_choices


User = get_user_model()


class TestCreate(test.APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user',
                                             email='user@example.com')
        self.client = test.APIClient()
        self.client.login(username='user', password='user')

    def test_post_not_authentication(self):
        self.client.logout()
        resp = self.client.post(reverse('contacts_list_create'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)

    def test_post(self):
        resp = self.client.post(reverse('contacts_list_create'), {
        })
        print(resp)

    def test_get(self):
        resp = self.client.get(reverse('contacts_list_create'), {
        })
        print(resp)

    def test_get_not_authenticated(self):
        self.client.logout()
        resp = self.client.get(reverse('contacts_list_create'))
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)


class TestUpdate(test.APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='user',
                                             email='user@example.com')
        self.contact = Contact.objects.create(user=self.user,
                                              account='marazmiki',
                                              type='vk')
        self.client = test.APIClient()
        self.client.login(username='user', password='user')
        self.url = reverse('contacts_detail', kwargs={'pk': self.contact.pk})

    def test_post_not_authentication(self):
        self.client.logout()
        resp = self.client.post(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, resp.status_code)


    def test_post_authentication(self):
        resp = self.client.post(self.url)
        print(resp)


class TestGetAvailableBackends(test.APITestCase):
    def test_1(self):
        print(get_available_backends())


class TestGetBackend(test.APITestCase):
    def test_1(self):
        print(get_backend('vk'))

    def test_(self):
        print(get_type_choices())
