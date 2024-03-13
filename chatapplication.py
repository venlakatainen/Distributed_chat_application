from chatwindow import ChatWindow
from message import Message

MY_USERNAME = "Me"

class ChatApplication:
    def __init__(self):
        self.chats = []
        self.chats.append(ChatWindow(user="Distributed chat"))
    
    def add_user_chat(self, user):
        self.chats.append(ChatWindow(user=user))

    def add_group_chat(self, group):
        self.chats.append(ChatWindow(group=group))

    def open_chat(self, chat_i):
        current_chat = self.chats[chat_i]
        current_chat.start()
        current_chat.add_message(Message("Welcome to the chat!", "System", "You"))
        current_chat.add_message(Message("Instructions here", "System", "You"))
        while True:
            current_chat.get_message()
