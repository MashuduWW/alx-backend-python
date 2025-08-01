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


# example edit view
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


def message_detail(request, message_id):
    root_message = get_object_or_404(Message, pk=message_id)
    thread = get_thread(root_message)

    return render(request, 'message_detail.html', {
        'thread': thread,
        'root': root_message
    })

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
    


from .models import Message

@login_required
def unread_inbox(request):
    unread_messages = Message.unread.for_user(request.user)

    return render(request, 'inbox_unread.html', {
        'messages': unread_messages
    })









