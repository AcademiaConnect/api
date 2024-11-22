from rest_framework import serializers


class EventSerializers(serializers.Serializer):
    title = serializers.CharField()
    dateInitial = serializers.DateTimeField()
    dateFinal = serializers.DateTimeField()
    location = serializers.CharField()
    description = serializers.CharField()
    user = serializers.CharField(required=False)

    read_only_fields = ['id']  # Define o campo `id` como somente leitura

    def update(self, instance, validated_data):
        # Atualiza os campos da instância com os dados validados
        instance.title = validated_data.get('title', instance.title)
        instance.dateInitial = validated_data.get('dateInitial', instance.dateInitial)
        instance.dateFinal = validated_data.get('dateFinal', instance.dateFinal)
        instance.location = validated_data.get('location', instance.location)
        instance.description = validated_data.get('description', instance.description)
        instance.save()  # Salva a instância atualizada no banco de dados
        return instance
