from django.db import models

class ChatRoom(models.Model):
    user1_id = models.IntegerField()  
    user2_id = models.IntegerField()  
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1_id', 'user2_id')

    


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    user = models.IntegerField()
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f'Message from User {self.user} in {self.chat_room}'
    

class Notification(models.Model):
    user = models.IntegerField(null=True, blank=True)
    another_user  = models.IntegerField(null=True, blank=True)
    follower = models.IntegerField(null=True, blank=True)
    post = models.IntegerField(null=True, blank=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)



class Online(models.Model):
    user = models.IntegerField()
    is_online = models.BooleanField(default=False) 
    last_active = models.DateTimeField(null=True, blank=True)
    
    
    
class MesssageView(models.Model):
    chat_room = models.ForeignKey(ChatRoom,  on_delete=models.CASCADE)
    user = models.IntegerField()
    view = models.BooleanField(default=False)
    
    