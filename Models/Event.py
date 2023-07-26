import uuid

class Event:

    def __init__(self, name, date, userId, location):
        self.id = str(uuid.uuid4().int)
        self.name = name
        self.location = location
        self.date = date
        self.hostID = userId
        self.active = True
        self.performers = []
        self.requestedPerformers = []