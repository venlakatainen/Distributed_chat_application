from datetime import datetime

class Message:
    def __init__(self, message: str, sender: str, receiver: str, group=None):
        self.message = message
        self.sender = sender
        self.receiver = receiver
        self.time = datetime.now()
        self.group = group

    def get_json(self):
        return {
            "message": self.message,
            "sender": self.sender,
            "receiver": self.receiver,
            "time": self.time,
            "group": self.group if self.group else "null"
        }
    
    def __str__(self):
        return f"[{self.time.strftime('%Y-%m-%d %H:%M')}] {self.sender}: {self.message}"
    