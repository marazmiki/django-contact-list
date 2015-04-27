# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import forms
from django_contact_list.models import Contact


class CreateContactForm(forms.ModelForm):
    class Meta(object):
        model = Contact
        exclude = ['user']
