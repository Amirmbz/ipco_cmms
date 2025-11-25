"""ASGI config for ipco_cmms project."""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipco_cmms.settings')
application = get_asgi_application()