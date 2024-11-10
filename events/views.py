from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Events
from .serializers import EventSerializers
from .controllers import get_event_by_gpt

class EventView(APIView):
    """
    API View para gerenciar eventos.

    Este endpoint permite criar, listar, atualizar e deletar eventos.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = EventSerializers

    def post(self, request):
        """
        Cria um novo evento.

        **URL:** `/events/create/`  
        **Método HTTP:** `POST`  
        **Autenticação:** Necessária (Token JWT)

        **Corpo da Requisição (JSON):**
        ```json
        {
            "title": "string",
            "dateInitial": "YYYY-MM-DDTHH:MM:SSZ",
            "dateFinal": "YYYY-MM-DDTHH:MM:SSZ",
            "location": "string",
            "description": "string"
        }
        ```

        **Resposta de Sucesso (201 Created):**
        ```json
        {
            "id": "int",
            "title": "string",
            "dateInitial": "datetime",
            "dateFinal": "datetime",
            "location": "string",
            "description": "string",
            "user": "int"
        }
        ```

        **Erros Possíveis:**
        - **400 Bad Request:** Dados inválidos ou ausentes.
        - **401 Unauthorized:** Token inválido ou ausente.
        """
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

        event_serializer = self.serializer_class(event)

        return Response(data=event_serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        """
        Lista todos os eventos.

        **URL:** `/events/create/`  
        **Método HTTP:** `GET`  
        **Autenticação:** Necessária (Token JWT)

        **Resposta de Sucesso (200 OK):**
        ```json
        [
            {
                "id": "int",
                "title": "string",
                "dateInitial": "datetime",
                "dateFinal": "datetime",
                "location": "string",
                "description": "string",
                "user": "int"
            },
            ...
        ]
        ```

        **Erros Possíveis:**
        - **401 Unauthorized:** Token inválido ou ausente.
        """
        events = Events.objects.all()
        event_serializer = self.serializer_class(events, many=True)
        return Response(data=event_serializer.data, status=status.HTTP_200_OK)

    def put(self, request, event_id):
        """
        Atualiza um evento existente.

        **URL:** `/events/update/<int:event_id>/`  
        **Método HTTP:** `PUT`  
        **Autenticação:** Necessária (Token JWT)

        **Parâmetros de URL:**
        - `event_id` (int): ID do evento a ser atualizado.

        **Corpo da Requisição (JSON):**
        ```json
        {
            "title": "string",
            "dateInitial": "YYYY-MM-DDTHH:MM:SSZ",
            "dateFinal": "YYYY-MM-DDTHH:MM:SSZ",
            "location": "string",
            "description": "string"
        }
        ```

        **Resposta de Sucesso (200 OK):**
        ```json
        {
            "id": "int",
            "title": "string",
            "dateInitial": "datetime",
            "dateFinal": "datetime",
            "location": "string",
            "description": "string",
            "user": "int"
        }
        ```

        **Erros Possíveis:**
        - **400 Bad Request:** Dados inválidos ou ausentes.
        - **401 Unauthorized:** Token inválido ou ausente.
        - **403 Forbidden:** Usuário não autorizado a modificar este evento.
        - **404 Not Found:** Evento não encontrado.
        """
        event = get_object_or_404(Events, id=event_id, user=request.user)
        serializer = self.serializer_class(event, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, event_id):
        """
        Apaga um evento existente.

        **URL:** `/events/delete/<int:event_id>/`  
        **Método HTTP:** `DELETE`  
        **Autenticação:** Necessária (Token JWT)

        **Parâmetros de URL:**
        - `event_id` (int): ID do evento a ser apagado.

        **Resposta de Sucesso (204 No Content):**
        - Sem conteúdo no corpo da resposta.

        **Erros Possíveis:**
        - **401 Unauthorized:** Token inválido ou ausente.
        - **403 Forbidden:** Usuário não autorizado a deletar este evento.
        - **404 Not Found:** Evento não encontrado.
        """
        event = get_object_or_404(Events, id=event_id, user=request.user)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EventAutoFillView(APIView):
    """
    API View para auto-completar detalhes de eventos utilizando GPT.

    Este endpoint gera detalhes do evento com base em um texto fornecido.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Gera detalhes de um evento com base em um texto fornecido.

        **URL:** `/events/auto_complete/`  
        **Método HTTP:** `POST`  
        **Autenticação:** Necessária (Token JWT)

        **Corpo da Requisição (JSON):**
        ```json
        {
            "text": "string"
        }
        ```

        **Resposta de Sucesso (200 OK):**
        ```json
        {
            // Detalhes do evento gerados automaticamente
        }
        ```

        **Erros Possíveis:**
        - **400 Bad Request:** Dados inválidos ou ausentes.
        - **401 Unauthorized:** Token inválido ou ausente.
        - **404 Not Found:** Texto não fornecido ou inválido.
        """
        text = request.data.get('text')

        if not text:
            return Response({'message': 'Text not found'}, status=status.HTTP_404_NOT_FOUND)

        autoFill = get_event_by_gpt(text)

        return Response(autoFill, status=status.HTTP_200_OK)
