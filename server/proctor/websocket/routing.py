from django.urls import path
from websocket import consumers

urlpatterns = [
    path('ws/examinee/<str:examinee_id>', consumers.ExamineeConsumer.as_asgi()),
]
