from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['participants__username']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        conversation = serializer.save()
        return Response(ConversationSerializer(conversation).data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['sent_at']
    ordering = ['-sent_at']

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
