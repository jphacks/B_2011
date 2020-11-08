from django.urls import path
from websocket import consumers

urlpatterns = [
    path('ws/examinee/<str:room_name>', consumers.ExamineeConsumer.as_asgi()),
]
