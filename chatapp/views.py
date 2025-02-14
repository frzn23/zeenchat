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
import json
from .forms import CustomUserForm
from .redis_manager import update_user_status, get_user_status, get_redis_client
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    template_name = 'chatapp/login.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # Set user as online after successful login
        update_user_status(self.request.user.username, 'online')
        return response

def logout_view(request):
    if request.user.is_authenticated:
        update_user_status(request.user.username, 'offline')
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
    # Get active users excluding current user
    active_users = User.objects.filter(
        is_superuser=False
    ).exclude(
        id=request.user.id
    ).only(
        'id', 'username'
    ).order_by('username')
    
    # fetch all user statuses from redis
    redis = get_redis_client()
    pipeline = redis.pipeline()
    
    # Queue status lookups
    for user in active_users:
        key = f"user_status:{user.username}"
        pipeline.get(key)
    
    # Execute all status lookups at once
    user_statuses = pipeline.execute()
    
    # Combine user data with their status
    users_with_status = [
        {
            'user': user,
            'status': status or 'offline'  # status is already decoded since decode_responses=True
        }
        for user, status in zip(active_users, user_statuses)
    ]
    
    return render(request, 'chatapp/users.html', {
        'users': users_with_status
    })


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
    try:
        other_user = User.objects.get(username=username)
        messages = Message.objects.filter(
            (models.Q(sender=request.user, receiver=other_user) |
             models.Q(sender=other_user, receiver=request.user))
        ).order_by('timestamp')

        return render(request, 'chatapp/chat.html', {
            'other_user': other_user,
            'messages': messages
        })
    except User.DoesNotExist:
        return redirect('users')  # safe guard to redirect to users page if user does not exist
