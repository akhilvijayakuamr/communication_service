from django.http import JsonResponse
from django.views import View
from .models import ChatRoom, Message, Notification, Online, MesssageView, Premium
from django.db.models import Q
from .serializers import MessageSerializer, NotificationSerializer
from django.utils import timezone
from . email import send_mail


# Create Room View

def create_room(data):
    sender_id= data['sender_id']
    receiver_id = data['receiver_id']
    chat_room, created = ChatRoom.objects.get_or_create(user1_id=int(sender_id), user2_id=int(receiver_id))
    view, created = MesssageView.objects.get_or_create(chat_room=chat_room, user=sender_id)
    view.view = True
    view.save()
    return "success"



# Save Messages

def save_message(data):
    sender_id= data['sender_id']
    receiver_id = data['receiver_id']
    message_content = data['message_content']
    chat_room = ChatRoom.objects.get(user1_id=int(sender_id), user2_id=int(receiver_id))
    chat_room.created_at = timezone.now()
    chat_room.save()
    message = Message.objects.create(
        chat_room = chat_room,
        user = sender_id,
        content = message_content
    )
    try:
        chat_room2 = ChatRoom.objects.get(user1_id=int(receiver_id), user2_id=int(sender_id))
        view = MesssageView.objects.filter(chat_room=chat_room2, user=int(receiver_id), view=True).exists()
        if view:
            message.read=True
            message.save()
    except:
        pass
    
    online = Online.objects.filter(user=int(receiver_id), is_online=True).exists()
    
    return online




# Message details

def message_details(data):
    message_content = data.get('message_content')
    message = Message.objects.filter(content=message_content).order_by('-timestamp').first()
    
    if not message:
        return None
    message_obj = {
        'id': message.id,
        'chat_room': message.chat_room.id,
        'user': message.user,  
        'content': message.content,
        'timestamp': message.timestamp.isoformat(),
        'read':message.read
    }
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
            return []
    


# Get all chat user

def all_chat_user(data):
    try:
        user_id = int(data['user_id']) 
    except AttributeError:
        return []
    try:
        users = ChatRoom.objects.filter(
            Q(user1_id=user_id) | Q(user2_id=user_id)
        ).order_by('-created_at')
    except ChatRoom.DoesNotExist:
        return []
    
    chat_friends = []
    for user in users:
       
        if user.user1_id == user_id:
            if not any(user.user2_id in item for item in chat_friends):
                message = Message.objects.filter(chat_room=user, user = user.user2_id, read = False).count()
                online = Online.objects.filter(user=user.user2_id, is_online=True).exists()
                chat_friends.append([user.user2_id, str(message), online])
        elif user.user2_id == user_id:
            if not any(user.user1_id in item for item in chat_friends):
                message = Message.objects.filter(chat_room=user, user = user.user1_id, read = False).count()
                online = Online.objects.filter(user=user.user1_id, is_online=True).exists()
                chat_friends.append([user.user1_id, str(message), online])
    return chat_friends


# Save the follow notification

def follow_notification(data):
    user_id = int(data['user_id'])
    another_user_id = int(data['another_user_id'])
    notification = Notification.objects.create(
        user = another_user_id,
        another_user = user_id,
        follower = user_id,
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
            return []
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
        return 'Read all notification'
    



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
    if id:
        user, created = Online.objects.get_or_create(user=id)
        user.is_online = True
        user.last_active = timezone.now()
        user.save()
        chat_room = ChatRoom.objects.filter( Q(user1_id=id) | Q(user2_id=id))
        room_list = []
        for user in chat_room:
            room_list.append({user.user1_id, user.user2_id})
        return room_list
    else:
        return "failed"


# User is offline

def user_offline(data):
    id = int(data['user_id'])
    if id:
        user, created = Online.objects.get_or_create(user=id)
        user.is_online = False
        user.last_active = timezone.now()
        user.save()
        chat_room = ChatRoom.objects.filter( Q(user1_id=id) | Q(user2_id=id))
        room_list = []
        for user in chat_room:
            room_list.append({user.user1_id, user.user2_id})
        return room_list
    else:
        return "failed"
    
    
    
    
# check user is online

def check_online(data):
    try:
        user_id = int(data['user_id'])
        online = Online.objects.filter(user = user_id, is_online = True).exists()
        return online 
    except AttributeError:
        return False
    
    

# unview user

def user_unview(data):
    sender_id= data['sender_id']
    receiver_id = data['receiver_id'] 
    chat_room = ChatRoom.objects.get(user1_id=int(sender_id), user2_id=int(receiver_id))
    view, created = MesssageView.objects.get_or_create(chat_room=chat_room, user=sender_id)
    view.view = False
    view.save()
    return "unview"



# premium data store

def premium(data):
    customer_id = data['customer_id'][0] if isinstance(data['customer_id'], tuple) else data['customer_id']
    email = data['email'][0] if isinstance(data['email'], tuple) else data['email']
    amount = data['amount'][0] if isinstance(data['amount'], tuple) else data['amount']
    currency = data['currency'][0] if isinstance(data['currency'], tuple) else data['currency']
    status = data['status'][0] if isinstance(data['status'], tuple) else data['status']
    
    print(type(customer_id),"===", customer_id, type(email),"===", email,type(amount),"===", email,type(currency),"=====",currency, type(status),"===",status)
    
    payment, create = Premium.objects.get_or_create(
        customer_id = customer_id,
        email = email,
        amount = int(amount),
        currency = currency,
        status = status
    )
    
    payment.save()
    
    if create:
        subject = 'Payment Successful: Your Payment Has Been Processed'
        message = f"""
        Dear Customer,

        We are pleased to inform you that your payment has been successfully processed.

        Payment Details:
        Amount: {amount} {currency}
        Payment Status: {status}

        Thank you for your payment. We appreciate your business!

        Best regards,
        Assure Tech
        """ 
        
        return send_mail(email, subject, message)
          
    elif payment.status != 'paid':   
        
        subject = 'Payment Warning: Payment Status Not Successful'
        message = f"""
        Dear Customer,

        We noticed that your payment was not successful.

        Payment Details:
        Amount: {amount} {currency}
        Payment Status: {status}

        Please check your payment method or contact support for assistance.

        Best regards,
        Assure Tech
        """
        
        return send_mail(email, subject, message)
    
    else:
        return "Email is not send successfully"
    
    


# Premium user


def premium_user(data):
    try:
        email = str(data['email'])
        premium = Premium.objects.filter(email=email).exists()
        return premium
    except AttributeError:
        return False


    


               
     





    
    