from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from exams.models import Exam
from exams.serializers import ExamSerializer
import json


class ExamAPIView(APIView):

    def get(self, request, *args, **kwargs):

        exam = Exam.objects.get(*args, **kwargs)
        serializer = ExamSerializer(exam)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = ExamSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ExamListAPIView(APIView):

    def get(self, request, *args, **kwargs):
        exams = Exam.objects.all()
            #.filter(examinee_id=query_param_examinee_id) \a
            #.filter(alert=True)
        serializer = ExamSerializer(exams, many=True)
        data = {'exam_data': serializer.data}
        return Response(json.dumps(data), status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        serializer = ExamSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_201_CREATED)
