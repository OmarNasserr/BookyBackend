from asyncio.windows_events import NULL
from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from ..models import Playground
from ..serializers import PlaygroundSerializer
from helper_files.permissions import AdminOnly
from helper_files.status_code import Status_code
from ..validations import PlaygroundAppValidations


class PlaygroundCreate(generics.CreateAPIView):
    queryset = Playground.objects.all()
    serializer_class = PlaygroundSerializer
    permission_classes=[AdminOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        valid,err=serializer.is_valid(raise_exception=False)
        response = PlaygroundAppValidations.validate_playground_create(self.request.data,valid,err)
        if response.status_code == Status_code.created:
            serializer.save()

        return response