from django.urls import re_path
from .consumers import MyConsumer, DroneTelemetryConsumer

websocket_urlpatterns = [
    re_path(r'ws/test/$', MyConsumer.as_asgi()),
    re_path(r'ws/telemetry/(?P<drone_id>[^/]+)/$', DroneTelemetryConsumer.as_asgi()),
]

