"""
ASGI config for wordle_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set default settings module for the 'django' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wordle_project.settings')

# Get ASGI application for serving Django.
application = get_asgi_application()
