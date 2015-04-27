# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django import template
from django_contact_list.forms import CreateContactForm


register = template.Library()


@register.assignment_tag
def get_contact_formset(user):
    return [CreateContactForm(instance=i, prefix='i%s' % i.pk)
            for i in user.contacts.all()]


@register.assignment_tag
def create_contact_form():
    return CreateContactForm()
