# messaging/models.py
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

class MessageManager(models.Manager):
    def add_message(self, sender, content, thread):
        this = self.create(sender=sender, content=content, thread=thread)

        MessageCopy.objects.create(owner=sender, thread=thread, message=this)

    # def remove_message(self, sender, content, thread):
    #     pass

class MessageThread(models.Model):
    """ Message thread representation
    Fields:
        * `when` - a datetime stamp of when the thread is created
    """
    subject = models.CharField(max_length=255, blank=True)
    participants = models.ManyToManyField(User, related_name='message_threads')
    when = models.DateTimeField(auto_now_add=True)

# # Implementation for Quiting Threads
# class MessageThreadCopy(models.Model):
#     owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
#     thread = models.ForeignKey(MessageThread,
#                                on_delete=models.CASCADE,
#                                related_name='thread_copy')

#     message = models.ForeignKey(Message, on_delete=models.CASCADE)

#     is_removed = models.BooleanField(default=False)

#     # For when user quits [INCOMPLETE]
#     def remove_participation(self):
#         thread.participants.remove(owner)

#         models.CASCADE

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.SET_NULL,
                               related_name='sender', null=True)

    thread = models.ForeignKey(MessageThread,
                               on_delete=models.CASCADE,
                               related_name='thread')
    
    content = models.CharField(max_length=1000, blank=False)
    when = models.DateTimeField(auto_now_add=True)

    objects = MessageManager()

class MessageCopy(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner')
    thread = models.ForeignKey(MessageThread,
                               on_delete=models.CASCADE,
                               related_name='thread_copy')

    message = models.ForeignKey(Message, on_delete=models.CASCADE)

    is_removed = models.BooleanField(default=False)