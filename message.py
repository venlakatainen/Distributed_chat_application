from datetime import datetime

class Message:
    def __init__(self, message: str, sender: str, group: str = None, time: str = None):
        self.message = message
        self.sender = sender
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M') if not time else time
        self.group = group

    def get_json(self):
        return {
            "message": self.message,
            "sender": self.sender,
            "time": self.time,
           "group": self.group if self.group else "null"
        }
    
    def __str__(self):
        return f"[{self.time}] {self.sender}{f' in {self.group}' if self.group != 'null' else ''}: {self.message}"
    
    @staticmethod
    def from_json(json):
        return Message(json["message"], json["sender"], time=json["time"] if json["time"] else None, group=json["group"] if json["group"] else None)