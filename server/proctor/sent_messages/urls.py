from django.urls import path
from sent_messages import views

urlpatterns = [
    path('list', views.MessageListAPIView.as_view()),
    path('examlist', views.ExamIdListAPIView.as_view()),
]
