from django.core.asgi import get_asgi_application
from channels.security.websocket import OriginValidator
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
import os
import django
django.setup()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataupload.settings")
django_asgi_app = get_asgi_application()
from api.consumers import UploadConsumer, UploadDeleteConsumer, SMOrderConsumer  # noqa

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": OriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("ws/upload/<int:upload_id>/", UploadConsumer.as_asgi()),
                path("ws/delete-upload/<int:upload_id>/",
                     UploadDeleteConsumer.as_asgi()),
                path("ws/sm/orders/", SMOrderConsumer.as_asgi())
            ])
        ), ["http://localhost:3000", "https://www.dataupload.xyz", "https://cashflow.dataupload.xyz", "stock.dataupload.xyz"]
    ),
})
