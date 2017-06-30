# messaging/tests.py
from django.contrib.auth.models import User
from datetime import timedelta

from django.test import TestCase
from django.utils import timezone

from messaging.models import MessageThread, Message


class MessageThreadModelTestCase(TestCase):
    """ Tests for MessageThread model """
    def setUp(self):
        self.user1 = User.objects.create_user(username='User1', password='pass')
        self.user2 = User.objects.create_user(username='User2', password='pass')

    def test_thread_when(self):
        """Test the field `when`"""
        self.assertEqual(MessageThread.objects.count(), 0)
        tomorrow = timezone.now() + timedelta(days=1)
        self.assertEqual(
            MessageThread.objects.filter(when__gte=tomorrow).count(), 0)

    def test_thread_create(self):
        """Test creating a thread with subject and participants"""
        self.assertEqual(MessageThread.objects.count(), 0)
        self.assertEqual(self.user1.message_threads.count(), 0)
        self.assertEqual(self.user2.message_threads.count(), 0)

        thread = MessageThread.objects.create(subject='Lunch')
        thread.participants.add(self.user1, self.user2)
        self.assertEqual(MessageThread.objects.count(), 1)
        self.assertEqual(self.user1.message_threads.count(), 1)
        self.assertEqual(self.user2.message_threads.count(), 1)

    def test_message_create(self):
        """Test creating of message. Find a way to refer `sender`, `content`, `when`"""
        thread = MessageThread.objects.create(subject='Lunch')
        # here, `add_message` is a model manager method
        Message.objects.add_message(
            sender=self.user1, content="Guys, let's eat!",
            thread=thread)
        # To reply
        Message.objects.add_message(
            sender=self.user2, content='Alright!',
            thread=thread)


        self.assertEqual(Message.objects.count(), 2)
        self.assertEqual(MessageThread.objects.count(), 1)

    def test_message_copy(self):
        """Test creating of message now providing a copy to each recipient.
        When a message is marked removed we don't really remove the Message
        instance but only the user's copy of that instance.
        A user copy may have `owner`, `message`, `thread` and a boolean `is_removed`
        """
        thread = MessageThread.objects.create(subject='Lunch')

        self.assertEqual(MessageThread.objects.count(), 1)

        Message.objects.add_message(
            sender=self.user1, content="Guys, let's eat!",
            thread=thread)

        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(MessageCopy.objects.count(), 2)

        # pass