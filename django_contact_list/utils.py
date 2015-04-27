# coding: utf-8

from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from django.utils.module_loading import import_string
from django_contact_list import settings


def get_available_backends():
    backends = ()

    for key, val in settings.BACKENDS:
        if isinstance(val, (tuple, list)):
            for code, back in val:
                backends += (
                    (code, back),
                )
            continue
        backends += (
            (key, back),
        )
    return backends


def get_type_choices():
    choices = ()

    for key, val in settings.BACKENDS:
        if isinstance(val, (tuple, list)):
            group = ()
            for code, back in val:
                group += (
                    (code, backend_title(back)),
                )
            choices += (
                (key, group),
            )
        else:
            choices += (
                (key, backend_title(val)),
            )
    return choices


def get_backend(backend_code):
    all_backends = dict(get_available_backends())
    backend = import_backend(all_backends[backend_code])
    return backend


def backend_title(backend):
    return import_backend(backend).title


def import_backend(backend):
    return import_string(backend)
