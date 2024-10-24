from rest_framework import serializers


class EventSerializers(serializers.Serializer):
    title = serializers.CharField()
    dateInitial = serializers.DateTimeField()
    dateFinal = serializers.DateTimeField()
    location = serializers.CharField()
    description = serializers.CharField()
    user = serializers.CharField(required=False)
