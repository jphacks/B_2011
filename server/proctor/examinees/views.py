from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from examinees.models import Examinee
from examinees.serizlizers import ExamineeSerializer
import json


class ExamineeListAPIView(APIView):
    def get(self, request, *args, **kwargs):

        exam_id = request.GET.get('exam_id')
        examinees = Examinee.objects.filter(exam_id=exam_id)
        serializer = ExamineeSerializer(examinees, many=True)
        data = {'examinee_data': serializer.data}

        return Response(json.dumps(data), status=status.HTTP_200_OK)
