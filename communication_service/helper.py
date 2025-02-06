from message.views import *



# Helper function

def perform_operation(data):
    
    operation = data['operation']
    
    if operation == 'create_room':
        return create_room(data)
    
    elif operation == "save_message":
        return save_message(data)
    
    elif operation == 'get_message':
        return message_details(data)
    
    elif operation == 'get_all_chat':
        return get_all_message(data)
    
    elif operation == 'all_chat_user':
        return all_chat_user(data)
    
    elif operation == 'follow_notification':
        return follow_notification(data)
    
    elif operation == 'like_notification':
        return like_notification(data)
    
    elif operation == 'comment_notification':
        return comment_notification(data)

    elif operation == 'all_notification':
        return get_notifications(data)
    
    elif operation == 'read_notification':
        return read_notifications(data)
    
    elif operation == 'get_notification':
        return notification_details(data)
    
    elif operation == 'user_online':
        return user_online(data)
    
    elif operation == 'user_offline':
        return user_offline(data)
    
    elif operation == 'online_user':
        return check_online(data)
    
    elif operation == 'user_unview':
        return user_unview(data)
    
    elif operation == 'premium':
        return premium(data)
    
    elif operation == 'premium_user':
        return premium_user(data)

        
        