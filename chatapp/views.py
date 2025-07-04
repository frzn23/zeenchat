# chatapp/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import models
from .models import Message, FriendRequest
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

    users_annotated = users.annotate(
        # if already friends
        is_friend = models.Exists(
            FriendRequest.objects.filter(
                models.Q(sender=request.user, receiver=models.OuterRef('pk')) |
                models.Q(receiver=request.user, sender=models.OuterRef('pk')),
                status=FriendRequest.Status.ACCEPTED
            )
        ),
        # if I've a pending request from them
        sent_pending = models.Exists(
            FriendRequest.objects.filter(
                sender=models.OuterRef('pk'),
                receiver=request.user,
                status=FriendRequest.Status.PENDING
            )
        ),
        # if I've sent them a request & is pending
        i_sent_request = models.Exists(
            FriendRequest.objects.filter(
                sender=request.user,
                receiver=models.OuterRef('pk'),
            )
        )
    ).select_related()

    chat_users = users_annotated.filter(is_friend=True)
    addable_users = users_annotated.filter(
        is_friend=False,
        sent_pending=False,
        i_sent_request=False
    )
    pending_requests = FriendRequest.objects.filter(
        receiver=request.user, 
        status=FriendRequest.Status.PENDING
    ).select_related('sender')

     
    return render(
        request, 
        'chatapp/users.html', 
        {
            'users': users,
            'chat_users': chat_users,
            'pending_requests': pending_requests,
            'addable_users': addable_users
        }
    )


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

    # mark message from other_user to current user as read
    Message.objects.filter(
        sender = other_user,
        receiver = request.user,
        is_read = False
    ).update(is_read=True)

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

@login_required
def get_unread_counts(request):
    """return a json unread message counts by sender"""
    unread_counts = Message.objects.filter(
        receiver=request.user,
        is_read=False
    ).values('sender__username').annotate(count=models.Count('id'))

    # Update this line to use sender__username instead of sender_username
    result = {item['sender__username']: item['count'] for item in unread_counts}
    print(result)
    return JsonResponse(result)

@login_required
def add_friend(request):
    """sends friend request"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user = User.objects.get(username=data['to_user'])

            FriendRequest.objects.create(
                sender=request.user,
                receiver=user   
            )

            return JsonResponse({'status': 'success', 'message': 'Friend request sent'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)

@login_required
def accept_or_decline_request(request, action):
    """accept friend requests"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            sender = User.objects.get(username=data['request_from_user'])
            
            # find the friend req obj associated with the users
            request_obj = FriendRequest.objects.get(
                sender=sender,
                receiver=request.user,
            )

            if action == 'accept':
                request_obj.status = FriendRequest.Status.ACCEPTED
                request_obj.save()
                # request_obj.refresh_from_db()
                return JsonResponse({'status': 'sucess', 'message': 'Friend request accepted'})

            # upon decline, we'd delete the request obj. so user will be again available to send request.
            if action == 'decline':
                request_obj.delete()
                return JsonResponse({'status': 'sucess', 'message': 'Friend request declined'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)
