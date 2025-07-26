
from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access.
    - Only participants of the conversation can view/send/update/delete messages.
    """

    def has_permission(self, request, view):
        # Require authentication for any access
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # For Conversation objects, check participants directly
        if hasattr(obj, 'participants'):
            return user in obj.participants.all()

        # For Message objects, check participants of the related conversation
        if hasattr(obj, 'conversation'):
            return user in obj.conversation.participants.all()

        # Default deny
        return False
