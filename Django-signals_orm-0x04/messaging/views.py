from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from .models import Message
from .utils import get_thread


User = get_user_model()

def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all().order_by('-edited_at')
    return render(request, 'message_history.html', {'message': message, 'history': history})


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, pk=message_id, sender=request.user)

    if request.method == "POST":
        new_content = request.POST['content']
        message.content = new_content
        message.edited_by = request.user
        message.save()
        return redirect('inbox')  # or wherever

    return render(request, 'edit_message.html', {'message': message})



@login_required
def delete_user(request):
    if request.method == "POST":
        user = request.user
        logout(request)         # End the session first
        user.delete()           # Delete the user from DB
        return redirect('account_deleted')  # Redirect to confirmation page
    return render(request, 'delete_user.html')  # Show a confirmation form




@login_required
def reply_message(request, parent_id):
    parent = get_object_or_404(Message, pk=parent_id)
    if request.method == "POST":
        Message.objects.create(
            sender=request.user,
            receiver=parent.receiver,
            content=request.POST['content'],
            parent_message=parent
        )
        return redirect('message_detail', message_id=parent_id)
    



@login_required
def unread_inbox(request):
    unread_messages = Message.unread.unread_for_user(request.user).only('id', 'sender', 'content', 'timestamp')
    return render(request, 'unread_inbox.html', {
        'messages': unread_messages
    })



def get_message_thread(message):
    """
    Recursively collects all replies to a message in a threaded format.
    Returns a list of (message, depth) tuples.
    """
    thread = []

    def recurse(msg, depth=0):
        thread.append((msg, depth))
        replies = msg.replies.select_related('sender').all().order_by('timestamp')
        for reply in replies:
            recurse(reply, depth + 1)

    recurse(message)
    return thread

@login_required
def message_detail(request, message_id):
    root = get_object_or_404(
        Message.objects.select_related('sender', 'receiver'),
        pk=message_id
    )

    thread = get_threaded_replies(root)

    return render(request, 'message_detail.html', {
        'root': root,
        'thread': thread
    })


def get_threaded_replies(root_message):
    """
    Recursively fetch all replies using Message.objects.filter
    and optimize with select_related for sender.
    Returns a list of (message, depth) tuples.
    """
    thread = []

    def recurse(message, depth):
        thread.append((message, depth))

        # ✅ Explicit use of Message.objects.filter
        replies = Message.objects.filter(parent_message=message).select_related('sender').order_by('timestamp')

        for reply in replies:
            recurse(reply, depth + 1)

    recurse(root_message, 0)
    return thread




