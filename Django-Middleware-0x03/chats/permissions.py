# chats/permissions.py

from rest_framework import permissions
from rest_framework.permissions import SAFE_METHODS

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission:
    - Only authenticated users can access the API.
    - Only participants of the conversation can view messages.
    - Only the sender can edit or delete a message.
    """

    def has_permission(self, request, view):
        # Require user to be authenticated
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        # Read permissions: Only participants can view
        if request.method in SAFE_METHODS:
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()

        # Write permissions: Only sender can update/delete a message
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            if hasattr(obj, 'sender'):
                return obj.sender == user
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()

        # Allow creating new messages if user is a participant
        if request.method == 'POST':
            if hasattr(obj, 'participants'):
                return user in obj.participants.all()
            if hasattr(obj, 'conversation'):
                return user in obj.conversation.participants.all()

        return False
