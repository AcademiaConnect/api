from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import EventSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Events
from rest_framework import status
from rest_framework.response import Response


class EventView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializers

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        title = serializer.validated_data.get('title')
        dateInitial = serializer.validated_data.get('dateInitial')
        dateFinal = serializer.validated_data.get('dateFinal')
        location = serializer.validated_data.get('location')
        description = serializer.validated_data.get('description')

        event = Events.objects.create(
            title=title,
            dateInitial=dateInitial,
            dateFinal=dateFinal,
            location=location,
            description=description,
            user=request.user
        )

        event_serializer  = EventSerializers(event)

        return Response(data=event_serializer.data, status=status.HTTP_201_CREATED)


    def get(self, request):
        events = Events.objects.all()

        event_serializer  = EventSerializers(events, many=True)

        return Response(data=event_serializer.data, status=status.HTTP_200_OK)
