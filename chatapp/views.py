# chatapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from .models import Message
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json
from .forms import CustomUserForm

def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users')
    else:
        form = CustomUserForm()
    return render(request, 'chatapp/signup.html', {'form': form})

@login_required
def users(request):
    users = User.objects.filter(is_superuser=False).exclude(id=request.user.id)
    return render(request, 'chatapp/users.html', {'users': users})


@csrf_exempt
def save_message(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sender = request.user
            receiver = User.objects.get(username=data['receiver'])

            message = Message(
                sender=sender,
                receiver=receiver,
            )
            message.content = data['message']  # Automatically encrypts
            message.save()

            return JsonResponse({
                'status': 'success',
                'message_id': message.id,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)


@login_required
def chat(request, username):
    other_user = User.objects.get(username=username)
    messages = Message.objects.filter(
        (models.Q(sender=request.user, receiver=other_user) |
         models.Q(sender=other_user, receiver=request.user))
    ).order_by('timestamp')
    
    paginator = Paginator(messages, 10) #number kept low for testing, set to optimal number of messages
    page_number = request.GET.get('page', paginator.num_pages)
    messages_page = paginator.get_page(page_number)

    if request.headers.get('HX-Request'):
        return render(request, 'chatapp/partials/message_list.html', {
            'messages': messages_page,
            'other_user': other_user
        })

    return render(request, 'chatapp/chat.html', {
        'other_user': other_user,
        'messages': messages_page  # content is auto-decrypted
    })
