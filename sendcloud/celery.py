from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sendcloud.settings')

from django.conf import settings

app = Celery('sendcloud')

# uppercase name-space means that all Celery configuration options must
# be specified in uppercase instead of lowercase, and start with CELERY
# so broker_url setting -> CELERY_BROKER_URL.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

