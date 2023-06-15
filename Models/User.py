import uuid

class User:
    def __init__(self, firstName, lastName, age):
        self._firstName = firstName
        self._lastName = lastName
        self._email = firstName.lower() + lastName.lower() + '@email.com'
        self._age = age
        self._active = True
        self._id = str(uuid.uuid4().int)
        self._username = firstName.lower() + lastName.lower()
        self._password = 'pass123'

    def printUserInfo(self):
        print(self._firstName)
        print(self._lastName)
        print(self._email)
        print(self._age)
        print('Active: ' + str(self._active))
