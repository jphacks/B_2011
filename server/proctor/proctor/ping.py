from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class PingAPIView(APIView):

    def get(self, request, *args, **kwargs):

        return Response(None, status=status.HTTP_200_OK)
