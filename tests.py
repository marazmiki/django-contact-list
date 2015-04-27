#!/usr/bin/env python
# coding: utf-8

from django.conf import settings
import sys
import os


sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


settings.configure(
    ROOT_URLCONF='django_contact_list.urls',
    INSTALLED_APPS=(
        'django.contrib.sessions',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django_contact_list',
        'rest_framework',
    ),
    MIDDLEWARE_CLASSES=(
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
    ),
    TEMPLATE_LOADERS=(
        'django.template.loaders.filesystem.Loader',
        'django.template.loaders.app_directories.Loader',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':MEMORY:'
        }
    },
    REST_FRAMEWORK={
        'DEFAULT_AUTHENTICATION_CLASSES': (
            'rest_framework.authentication.BasicAuthentication',
            'rest_framework.authentication.SessionAuthentication',
        ),
    }
)


def main():
    from django.test.utils import get_runner
    import django

    if hasattr(django, 'setup'):
        django.setup()

    find_pattern = 'django_contact_list'

    test_runner = get_runner(settings)(verbosity=2, interactive=True,
                                       failfast=True)
    failed = test_runner.run_tests([find_pattern])
    sys.exit(failed)


if __name__ == '__main__':
    main()
