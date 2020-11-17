from django.urls import path
from websocket import consumers

urlpatterns = [
    path('ws/examinee/<str:exam_id>', consumers.ExamineeConsumer.as_asgi()),
    path('ws/user/<str:exam_id>', consumers.UserConsumer.as_asgi()),
]
