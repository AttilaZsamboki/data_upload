from django.urls import path

from api import consumers

websocket_urlpatterns = [
    path('ws/upload/', consumers.UploadConsumer.as_asgi()),
]
