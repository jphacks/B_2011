from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sent_messages.models import Message
from sent_messages.serizlizers import MessageSerializer
import json
import numpy as np


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
                .filter(examinee_id=query_param_examinee_id) \
                .order_by('-created_at')
            serializer = MessageSerializer(messages, many=True)
            data = {'alert_data': serializer.data}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        if query_param_exam_id:
            messages = Message.objects \
                .filter(exam_id=query_param_exam_id) \
                .order_by('-created_at')
            serializer = MessageSerializer(messages, many=True)
            data = {'alert_data':  serializer.data}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_201_CREATED)


class MessageTimeListAPIView(APIView):

    def get(self, request, *args, **kwargs):

        query_param_examinee_id = request.GET.get('examinee_id')
        query_param_exam_id = request.GET.get('exam_id')
        if query_param_examinee_id:
            time_list = Message.objects \
                .filter(examinee_id=query_param_examinee_id) \
                .order_by('-created_at') \
                .values_list('created_at', flat=True)
            module_list = Message.objects \
                .filter(examinee_id=query_param_examinee_id) \
                .order_by('-created_at') \
                .values_list('module_name', flat=True)

            time_array = np.array(list(map(format_time, time_list)))
            module_array = np.array(list(map(format_module, list(module_list))))
            time_list = np.vstack((time_array, module_array)).T.tolist()
            data = {'time_list': time_list}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        if query_param_exam_id:
            time_list = Message.objects \
                .filter(exam_id=query_param_exam_id) \
                .order_by('-created_at') \
                .values_list('created_at', flat=True)
            module_list = Message.objects \
                .filter(exam_id=query_param_exam_id) \
                .order_by('-created_at') \
                .values_list('module_name', flat=True)

            time_list = list(map(format_time, list(time_list)))
            module_list = list(map(format_module, list(module_list)))
            data = {'time_list': time_list, 'module_list': module_list}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)


module_map = {'activewindow':0, 'clipboard':1, 'electron-activewindow':2, 'electron-clipboard':3}


def format_time(time):
    return int(time.timestamp())


def format_module(module_name):
    return module_map[module_name]

