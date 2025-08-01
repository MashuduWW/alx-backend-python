from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from .models import Message

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



def account_deleted(request):
    return render(request, 'account_deleted.html')










