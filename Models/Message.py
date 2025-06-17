import uuid

class Message:

    def __init__(self, subject, message, userId):
        self.id = str(uuid.uuid4().int)
        self.date = '7/25/2023'
        self.subject = subject
        self.message = message
        self.userId = userId
        self.read = False
