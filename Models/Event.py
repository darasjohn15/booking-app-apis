import uuid

class Event:

    def __init__(self, title, date, host_id, venue_id, description=""):
        self.id = str(uuid.uuid4().int)
        self.title = title
        self.date = date
        self.host_id = host_id
        self.venue_id = venue_id
        self.description = description
        self.active = True
        self.applications = []
        self.performers = []