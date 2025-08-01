from django.db.models.signals import post_save, pre_save, post_delete
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory



User = get_user_model()


@receiver(post_save, sender=Message)
def create_notification_on_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            user=instance.receiver,
            message=instance
        )


# signals.py
@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if not instance.pk:
        return  # New message, not an edit

    try:
        old = Message.objects.get(pk=instance.pk)
    except Message.DoesNotExist:
        return

    if old.content != instance.content:
        MessageHistory.objects.create(
            message=instance,
            old_content=old.content,
            edited_by=instance.edited_by  # Track editor
        )
        instance.edited = True




@receiver(post_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    # Delete messages where user is either sender or receiver
    Message.objects.filter(sender=instance).delete()
    Message.objects.filter(receiver=instance).delete()

    # Delete notifications (redundant if FK uses CASCADE)
    Notification.objects.filter(user=instance).delete()







