from django.urls import path
from exams import views

urlpatterns = [
    path('list', views.ExamListAPIView.as_view()),
]
