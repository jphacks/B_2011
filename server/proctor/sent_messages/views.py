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
                .filter(examinee_id=query_param_examinee_id, alert__gt=0) \
                .order_by('-created_at')
            serializer = MessageSerializer(messages, many=True)
            data = {'alert_data': serializer.data[0:50]}
            return Response(json.dumps(data), status=status.HTTP_200_OK)

        if query_param_exam_id:
            messages = Message.objects \
                .filter(exam_id=query_param_exam_id, alert__gt=0) \
                .order_by('-created_at')
            serializer = MessageSerializer(messages, many=True)
            data = {'alert_data':  serializer.data[0:50]}
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
            # list for normal
            time_list_normal = time_list_by_examinee(query_param_examinee_id, 0)
            # list for warning
            time_list_warning = time_list_by_examinee(query_param_examinee_id, 1)
            # list for warning
            time_list_alert = time_list_by_examinee(query_param_examinee_id, 2)

            data = {'time_list_normal': time_list_normal,
                    'time_list_warning': time_list_warning,
                    'time_list_alert': time_list_alert}

            return Response(json.dumps(data), status=status.HTTP_200_OK)

        if query_param_exam_id:
            # list for normal
            time_list_normal = time_list_by_exam(query_param_exam_id, 0)
            # list for warning
            time_list_warning = time_list_by_exam(query_param_exam_id, 1)
            # list for warning
            time_list_alert = time_list_by_exam(query_param_exam_id, 2)

            data = {'time_normal_list': time_list_normal,
                    'time_warning_list': time_list_warning,
                    'time_alert_list': time_list_alert}

            return Response(json.dumps(data), status=status.HTTP_200_OK)

        return Response(None, status=status.HTTP_400_BAD_REQUEST)


def time_list_by_exam(exam_id, alert_num):

    time_list = Message.objects \
        .filter(exam_id=exam_id, alert=alert_num) \
        .order_by('-created_at') \
        .values_list('created_at', flat=True)
    module_list = Message.objects \
        .filter(exam_id=exam_id, alert=alert_num) \
        .order_by('-created_at') \
        .values_list('module_name', flat=True)

    time_array = np.array(list(map(format_time, time_list)))
    module_array = np.array(list(map(format_module, list(module_list))))
    time_list = np.vstack((time_array, module_array)).T.tolist()

    return time_list[0:100]


def time_list_by_examinee(examinee_id, alert_num):

    time_list = Message.objects \
        .filter(examinee_id=examinee_id, alert=alert_num) \
        .order_by('-created_at') \
        .values_list('created_at', flat=True)
    module_list = Message.objects \
        .filter(examinee_id=examinee_id, alert=alert_num) \
        .order_by('-created_at') \
        .values_list('module_name', flat=True)

    time_array = np.array(list(map(format_time, time_list)))
    module_array = np.array(list(map(format_module, list(module_list))))
    time_list = np.vstack((time_array, module_array)).T.tolist()

    return time_list[0:100]


def format_time(time):
    return int((time.timestamp()+32400)*1000)


module_map = {'active_window': 1, 'clipboard': 2, 'face_recognition': 3, 'head_pose_estimation': 4,'voice_recognition': 5, 'second_screen': 6, 'ssh_process_name': 7, 'ssh_network_traffic': 8}


def format_module(module_name):
    return module_map[module_name]
