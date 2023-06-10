from django.shortcuts import render, redirect, HttpResponse
from .models import User, Message, Comment
from django.contrib import messages
import datetime



def wall(request):
    user_id = request.session.get('user_id')
    current_time = datetime.datetime.now()
    if user_id:
        context = {
            "user": User.objects.get(id=user_id),
            "msgs": Message.objects.all(),
            'current_time': current_time
        }
        return render(request, "wall.html", context)
    else:
        return redirect('/logout')


def post_msg(request):
    if request.method == 'POST':
        errors = Message.objects.validator_msg(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            message = request.POST.get('message')
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            Message.objects.create(content=message, user=user)
            messages.success(request, "Posted a new message successfully")
        return redirect('/wall')
    else:
        return HttpResponse('Method not allowed', status=405)


def post_cmt(request):
    if request.method == 'POST':
        errors = Comment.objects.validator_cmt(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            comment = request.POST.get('comment')
            user_id = request.session.get('user_id')
            user = User.objects.get(id=user_id)
            message_id = request.POST.get('message_id_cmt')
            message = Message.objects.get(id=message_id)
            Comment.objects.create(comment=comment, message=message, user=user)
            messages.success(request, "Posted a new comment successfully")
        return redirect('/wall')
    else:
        return HttpResponse('Method not allowed', status=405)


def destroy_msg(request):
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = Message.objects.get(id=message_id)
        if message.user.id == request.session.get('user_id'):
            current_time = datetime.datetime.now()
            time_difference = current_time - message.created_at
            if time_difference.total_seconds() <= 1800:
                message.delete()
                return redirect('/wall')
            else:
                messages.error(request, "You can only delete messages written within the last 30 minutes.")
        else:
            messages.error(request, "You can only delete your own messages.")
    else:
        return HttpResponse('Method not allowed', status=405)


def destroy_cmt(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        Comment.objects.get(id=comment_id).delete()
        return redirect('/wall')
    else:
        return HttpResponse('Method not allowed', status=405)