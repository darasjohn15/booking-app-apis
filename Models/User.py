import uuid

class User:

    def __init__(self, name, email, role, password, age):
        self.id = str(uuid.uuid4().int)
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.age = age
        self.active = True