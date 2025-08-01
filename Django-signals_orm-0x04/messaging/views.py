from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, logout
from .models import Message

User = get_user_model()

def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all().order_by('-edited_at')
    return render(request, 'message_history.html', {'message': message, 'history': history})


@login_required
def delete_user(request):
    user = request.user
    logout(request)  # End the session first
    user.delete()
    return redirect('account_deleted')  # Redirect to a success page



def account_deleted(request):
    return render(request, 'account_deleted.html')








