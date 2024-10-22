# views.py

from django.http import JsonResponse
from django.views import View
from .models import ChatRoom, Message, Notification, Online
from django.db.models import Q
from .serializers import MessageSerializer, NotificationSerializer
from django.utils import timezone



# Create Room View


def create_room(data):
    sender_id= data['sender_id']
    receiver_id = data['receiver_id']
    chat_room, created = ChatRoom.objects.get_or_create(user1_id=int(sender_id), user2_id=int(receiver_id))
    return "success"



# Save Messages



def save_message(data):
    sender_id= data['sender_id']
    receiver_id = data['receiver_id']
    message_content = data['message_content']
    chat_room = ChatRoom.objects.get(user1_id=int(sender_id), user2_id=int(receiver_id))
    chat_room.created_at = timezone.now()
    chat_room.save()
    Message.objects.create(
        chat_room = chat_room,
        user = sender_id,
        content = message_content
    )
    
    return "success"




# Message details


def message_details(data):
    message_content = data['message_content']
    message = Message.objects.filter(content = message_content).first()
    message_obj = {
        'id':message.id,
        'chat_room':message.chat_room.id,
        'user':message.user,
        'content':message.content,
        'timestamp':message.timestamp.isoformat(),
    }
    print(message_obj)
    return message_obj




# get all messages


def get_all_message(data):
    sender_id= data['sender_id']
    receiver_id = data['receiver_id']
    try:
        chat_room = ChatRoom.objects.filter(
            Q(user1_id = sender_id, user2_id = receiver_id) |
            Q(user1_id = receiver_id, user2_id = sender_id)
        )

        messages = Message.objects.filter(chat_room__in=chat_room)
        for message in messages:
            if(message.user != int(sender_id)):
                message.read = True
                message.save()

        messages = Message.objects.filter(chat_room__in=chat_room)
        serializer = MessageSerializer(messages, many=True)
        return serializer.data
        
        
    except ChatRoom.DoesNotExist:  
            return Message.objects.none()
    


# Get all chat user

def all_chat_user(data):
    user_id = int(data['user_id'])
    print("request user ", user_id)

    users = ChatRoom.objects.filter(
        Q(user1_id=user_id) | Q(user2_id=user_id)
    ).order_by('-created_at')

 
    print("chat user",users.values())

    chat_friends = []

    for user in users:
       
        if user.user1_id == user_id:
            if not any(user.user2_id in item for item in chat_friends):
                print("oiut")
                online = Online.objects.filter(user = user.user2_id, is_online = True).exists()
                chat_friends.append({user.user2_id, online})
        elif user.user2_id == user_id:
            if not any(user.user1_id in item for item in chat_friends):
                online = Online.objects.filter(user = user.user1_id, is_online = True).exists()
                chat_friends.append({user.user1_id, online})
    print("Friends",chat_friends)
    return chat_friends


# Save the follow notification


def follow_notification(data):
    user_id = int(data['user_id'])
    another_user_id = int(data['another_user_id'])
    notification = Notification.objects.create(
        user = user_id,
        another_user = another_user_id,
        follower = another_user_id,
        content = "follow"
    )
    return [another_user_id,notification.content]



# save the post like notification


def like_notification(data):
    user_id = int(data['user_id'])
    another_user_id = int(data['another_user_id'])
    post_id = int(data['post_id'])
    notification = Notification.objects.create(
        user = user_id,
        another_user = another_user_id,
        post = post_id,
        content = 'liked'
    )
    return [user_id, notification.content]


# save the post comment notification


def comment_notification(data):
    user_id = int(data['user_id'])
    another_user_id = int(data['another_user_id'])
    post_id = int(data['post_id'])
    notification = Notification.objects.create(
        user = user_id,
        another_user = another_user_id,
        post = post_id,
        content = 'commented'
    )
    return [user_id,notification.content]


# get all notification


def get_notifications(data):
    id = data['user_id']
    if id:
        user_id = int(id)
        try:
            notifications = Notification.objects.filter(
                user = user_id
            ).order_by('-timestamp')
            serializer = NotificationSerializer(notifications, many=True)
            return serializer.data
        except Notification.DoesNotExist:
            return Message.objects.none()
    else:
        return []



# Read all notification


def read_notifications(data):
    user_id = int(data['user_id'])
    try:
        notifications = Notification.objects.filter(
            user = user_id, read = False
        )
        for notification in notifications:
            notification.read = True
            notification.save()
        return 'Read all notification'
    except Notification.DoesNotExist:
        return Message.objects.none()
    




# Message details


def notification_details(data):
    notification_content = data['notification_content']
    notification = Notification.objects.filter(content = notification_content).order_by('-timestamp').first()
    notification_obj = {
        'id':notification.user,
        'content':notification.content,
        'another_user':notification.another_user,
        'follower':notification.follower if notification.follower else None,
        'post':notification.post if notification.post else None,
        'read':notification.read,
        'timestamp':notification.timestamp.isoformat(),
    }
    return notification_obj



# User online

def user_online(data):
    id = int(data['user_id'])
    print("online", id)
    if id:
        user, created = Online.objects.get_or_create(user=id)
        if not created:
            user.is_online = True
            user.last_active = timezone.now()
            user.save()
            return "online"
        else:
            user.is_online = True
            user.last_active = timezone.now()
            user.save()
            return "online"
    else:
        return "failed"


# User is offline

def user_offline(data):
    id = int(data['user_id'])
    print("ofline", id)
    if id:
        user, created = Online.objects.get_or_create(user=id)
        if not created:
            user.is_online = False
            user.last_active = timezone.now()
            user.save()
            return "offline"
        else:
            user.is_online = False
            user.last_active = timezone.now()
            user.save()
            return "offline"
    else:
        return "failed"

    


               
     





    
    