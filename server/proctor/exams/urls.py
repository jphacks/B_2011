from django.urls import path
from exams import views

urlpatterns = [
    path('', views.ExamAPIView.as_view()),
    path('list', views.ExamListAPIView.as_view()),
]
