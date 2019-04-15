# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import PollRetrieveSerializer


class PollViewSet(viewsets.GenericViewSet):

    def retrieve(self, request, pk=None):
        serializer = PollRetrieveSerializer(data={'poll_id': pk})
        serializer.is_valid(raise_exception=True)
        response = serializer.retrieve()
        return Response(response)

    @action(detail=True, methods=['GET'])
    def hourly(self, request, pk=None):
        serializer = PollRetrieveSerializer(data={'poll_id': pk, 'hourly': True})
        serializer.is_valid(raise_exception=True)
        response = serializer.retrieve()
        return Response(response)
