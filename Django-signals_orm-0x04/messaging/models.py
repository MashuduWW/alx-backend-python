from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import Prefetch
from .models import Message
from .managers import UnreadMessagesManager



User = get_user_model()

# messaging/models.py

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    edited_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='edited_messages')
    objects = models.Manager()  # Default manager
    read = models.BooleanField(default=False)
    unread = UnreadMessagesManager()  # Custom manager
    
    parent_message = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replies'
    )

    def __str__(self):
        return f"Message {self.id} from {self.sender}"


class MessageHistory(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE, related_name='history')
    old_content = models.TextField()
    edited_at = models.DateTimeField(auto_now_add=True)
    edited_by = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='edit_histories'
    )

    def __str__(self):
        return f'History for Message {self.message.id}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)



def inbox(request):
    # Root messages (no parent) with replies
    root_messages = Message.objects.filter(receiver=request.user, parent_message__isnull=True).select_related(
        'sender', 'receiver'
    ).prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender'))
    ).order_by('-timestamp')

    return render(request, 'inbox.html', {'messages': root_messages})

