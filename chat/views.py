# chat/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.views.decorators.http import require_POST, require_http_methods
import json
from .models import Room, Message


@login_required
def index(request):
    rooms = Room.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'rooms': rooms})


@login_required
def room(request, room_name):
    room, created = Room.objects.get_or_create(
        name=room_name,
        defaults={'created_by': request.user}
    )
    messages = Message.objects.filter(room=room).order_by('timestamp')[:50]
    return render(request, 'room.html', {
        'room_name': room_name,
        'room': room,
        'messages': messages,
    })


@login_required
@require_POST
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.user != request.user:
        return HttpResponseForbidden('You can only edit your own messages.')

    data = json.loads(request.body)
    new_content = data.get('content', '').strip()

    if not new_content:
        return JsonResponse({'error': 'Message cannot be empty.'}, status=400)

    message.content = new_content
    message.edited  = True
    message.save()

    return JsonResponse({
        'success': True,
        'content': message.content,
        'edited': message.edited,
    })


@login_required
@require_http_methods(['DELETE'])
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)

    if message.user != request.user:
        return HttpResponseForbidden('You can only delete your own messages.')

    message.delete()
    return JsonResponse({'success': True})


@login_required
@require_http_methods(['DELETE'])
def delete_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)

    if room.created_by != request.user:
        return HttpResponseForbidden('Only the room creator can delete this room.')

    room.delete()
    return JsonResponse({'success': True})


@login_required
@require_POST
def update_room(request, room_name):
    room = get_object_or_404(Room, name=room_name)

    if room.created_by != request.user:
        return HttpResponseForbidden('Only the room creator can edit this room.')

    data = json.loads(request.body)
    room.description = data.get('description', '').strip()
    room.save()

    return JsonResponse({'success': True, 'description': room.description})