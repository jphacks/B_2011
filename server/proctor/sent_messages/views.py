from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from sent_messages.models import Message
from sent_messages.serizlizers import MessageSerializer


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
        messages = Message.objects.filter(examinee_id=request.query_params['examinee_id'])
        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = MessageSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(None, status=status.HTTP_201_CREATED)

