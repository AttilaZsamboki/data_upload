import os
from django.urls import path
from api.consumers import UploadConsumer, UploadDeleteConsumer, UpdateCashflowPlannerTable
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
import django
django.setup()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dataupload.settings")
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("ws/upload/<int:upload_id>/", UploadConsumer.as_asgi()),
                path("ws/delete-upload/<int:upload_id>/",
                     UploadDeleteConsumer.as_asgi()),
                path("ws/make_cashflow_planner/", UpdateCashflowPlannerTable)
            ])
        )
    ),
})
