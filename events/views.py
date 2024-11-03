from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import EventSerializers
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Events
from rest_framework import status
from rest_framework.response import Response
from .controllers import get_event_by_gpt


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

class EventAutoFillView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get('text')

        if not text:
            return Response({'message': 'Text not found'}, status=status.HTTP_404_NOT_FOUND)

        autoFill = get_event_by_gpt(text)

        return Response(autoFill, status=status.HTTP_200_OK)