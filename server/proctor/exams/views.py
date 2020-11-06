from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exams.models import Exam
from exams.serializers import ExamSerializer


class ExamAPIView(APIView):

    def get(self, request, *args, **kwargs):

        message = Exam.objects.get(*args, **kwargs)
        serializer = ExamSerializer(message)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = ExamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExamListAPIView(APIView):

    def get(self, request, *args, **kwargs):

        exams = Exam.objects.all()
        serializer = ExamSerializer(exams, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = ExamSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        #
        return Response(None, status=status.HTTP_201_CREATED)
