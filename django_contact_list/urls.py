# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.conf.urls import url
from django_contact_list.views import ContactListView, ContactDetailView


urlpatterns = [
    url(r'^$', ContactListView.as_view(), name='contacts_list_create'),
    url(r'^(?P<pk>\d+)/$', ContactDetailView.as_view(),
        name='contacts_detail'),
]
