from django.urls import path

from api.consumers import UploadConsumer

websocket_urlpatterns = [
    path('ws/upload/', UploadConsumer.as_asgi())
]
