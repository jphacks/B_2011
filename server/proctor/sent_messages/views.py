from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sent_messages.models import Message
from sent_messages.serizlizers import MessageSerializer
import json


class MessageAPIView(APIView):

    def get(self, request, *args, **kwargs):

        message = Message.objects.get(*args, **kwargs)
        serializer = MessageSerializer(message)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        user_id = request.user.user_id
        request.data['user_id'] = user_id
        serializer = MessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageListAPIView(APIView):

    def get(self, request, *args, **kwargs):

        query_param_examinee_id = request.GET.get('examinee_id')
        query_param_exam_id = request.GET.get('exam_id')
        if query_param_examinee_id:
            messages = Message.objects\
                .filter(examinee_id=query_param_examinee_id)\
                .filter(alert=True)
            serializer = MessageSerializer(messages, many=True)
            data = {'alert_data': serializer.data}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        if query_param_exam_id:
            messages = Message.objects \
                .filter(exam_id=query_param_exam_id) \
                .filter(alert=True)
            messages = MessageSerializer(messages, many=True)
            data = {'alert_data':  messages}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_201_CREATED)

