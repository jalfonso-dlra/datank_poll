# Create your views here.
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import PollCreateSerializer, VoteCreateSerializer


class PollViewSet(viewsets.GenericViewSet):

    def create(self, request):
        serializer = PollCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.create()
        return Response(response)

    @action(detail=True, methods=['POST'])
    def vote(self, request, pk=None):
        data = request.data
        data['poll_id'] = pk
        serializer = VoteCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        response = serializer.vote()
        return Response(response)
