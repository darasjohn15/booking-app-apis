import uuid

class Application:

    def __init__(self, event_id, event_title, performer_id, performer_name):
        self.id = str(uuid.uuid4().int)
        self.event_id = event_id
        self.event_title = event_title
        self.performer_id = performer_id
        self.performer_name = performer_name
        self.status = 'pending'