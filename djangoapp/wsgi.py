"""
WSGI config for djangoapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'djangoapp.settings'
sys.path.append('/home/djangoapp/djangoapp')
sys.path.append('/home/djangoapp')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djangoapp.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
