from django.urls import path
from exams import views

urlpatterns = [
    path('get', views.ExamAPIView.as_view()),
    path('list', views.ExamListAPIView.as_view()),
]
