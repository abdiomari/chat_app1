"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
# from channels.http import AsgiHandler
from channels.auth import AuthMiddleWareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import chat.routing

django_asgi_app = get_asgi_application()
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

application = ProtocolTypeRouter({
    "http" : django_asgi_app,
    "websocket" : AuthMiddleWareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
    ),
})
