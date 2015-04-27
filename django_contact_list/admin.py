# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.contrib import admin
from django_contact_list.models import Contact


class ContactAdmin(admin.ModelAdmin):
    search_fields = ['account']
    list_filter = ['type']
    list_display = ['__str__', 'user', 'type']


admin.site.register(Contact, ContactAdmin)
