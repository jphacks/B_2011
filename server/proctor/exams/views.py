from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exams.models import Exam
from exams.serializers import ExamSerializer
import json


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

        exam_list = list(Exam.objects.all().values_list('exam_id', flat=True))
        exam_list = list(map(str, exam_list))
        data = {'data': exam_list}
        return Response(json.dumps(data), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = ExamSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_201_CREATED)
