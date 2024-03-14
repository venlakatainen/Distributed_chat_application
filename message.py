from datetime import datetime

class Message:
    def __init__(self, message: str, sender: str, group: str = None, time: str = None):
        self.message = message
        self.sender = sender
        self.time = datetime.now().strftime('%Y-%m-%d %H:%M') if not time else time
        self.group = group

    def get_json(self):
        if self.group:
            return {
                "message": self.message,
                "sender": self.sender,
                "time": self.time,
                "group": self.group
            }
        return {
            "message": self.message,
            "sender": self.sender,
            "time": self.time
        }
    
    def __str__(self):
        if self.group:
            return f"[{self.time}] {self.sender} in {self.group}: {self.message}"
        return f"[{self.time}] {self.sender}: {self.message}"
    
    @staticmethod
    def from_json(json):
        if "group" not in json:
            return Message(json["message"], json["sender"], time=json["time"] if json["time"] else datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        return Message(json["message"], json["sender"], time=json["time"] if json["time"] else datetime.now().strftime('%Y-%m-%d %H:%M'), group=json["group"])