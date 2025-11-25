"""WSGI config for ipco_cmms project."""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipco_cmms.settings')
application = get_wsgi_application()