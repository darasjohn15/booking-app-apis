import uuid
import json

class User:
    def __init__(self, firstName, lastName, email, userName, password, age):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.age = age
        self.active = True
        self.id = str(uuid.uuid4().int)
        self.userName = userName
        self.password = password