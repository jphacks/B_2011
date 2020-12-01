from django.urls import path
from examinees import views

urlpatterns = [
    path('list', views.ExamineeListAPIView.as_view()),
]
