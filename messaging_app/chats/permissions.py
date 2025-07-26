# messaging_app/chats/permissions.py

from rest_framework import permissions

class IsParticipant(permissions.BasePermission):
    """
    Allows access only to users who are participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # Assumes obj is a Conversation or Message instance with participants
        user = request.user
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()
        elif hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()
        return False
