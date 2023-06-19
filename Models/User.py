import uuid

class User:
    def __init__(self, firstName, lastName, age):
        self.firstName = firstName
        self.lastName = lastName
        self.email = firstName.lower() + lastName.lower() + '@email.com'
        self.age = age
        self.active = True
        self.id = str(uuid.uuid4().int)
        self.userName = firstName.lower() + lastName.lower()
        self.password = 'pass123'
