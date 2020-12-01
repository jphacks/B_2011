from django.urls import path
from sent_messages import views

urlpatterns = [
    path('list', views.MessageListAPIView.as_view()),
    path('timelist', views.MessageTimeListAPIView.as_view()),
]
