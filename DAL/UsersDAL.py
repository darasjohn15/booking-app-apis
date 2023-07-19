from DAL.Database import DatabaseObject

class UsersDAL(DatabaseObject):

    def addUser(self, user):
        self._data.append(user)
        self.save()
        self.reload()
        print('')
        print('New User Created!')
        print('')

    def getUsers(self):
        return self._data

    def getUserById(self, id):
        for x in self._data:
            userid = x['id']
            if(id == userid):
                return x
            
    def getUserByUsername(self, userName):
        for x in self._data:
            if (userName == x['userName'] and x['active']):
                return x

    def updateUser(self, user):
        for x in self._data:
            if(x['id'] == user['id']):
                x = user
            else:
                continue

        print(self._data)

    def deactivateUser(self, id):
        index = 0
        deactivated = False
        
        for x in self._data:
            if (x['id'] == id):
                x['active'] = False
                self.save()
                self.reload()
                deactivated = True
                print('')
                print('User Deactivated!')
                print('')
                break

        if (not deactivated):
            print('')
            print('Invalid User ID...')
            print('')

    def editUser(self, userId, firstName, lastName, email, age):
        for x in self._data:
            if (x['id'] == userId):
                print('Users DAL: User Found!')
                x['firstName'] = firstName
                x['lastName'] = lastName
                x['email'] = email
                x['age'] = age
                self.save()
                self.reload()
                print('Users DAL: User Updated!')
                break

    def getPassword(self, userId):
        for x in self._data:
            if (x['id'] == userId):
                print('Users DAL: User Found!')
                return x['password']

    def changePassword(self, userId, newPassword):
        for x in self._data:
            if (x['id'] == userId):
                print('Users DAL: User Found!')
                x['password'] = newPassword
                self.save()
                self.reload()
                print('Users DAL: Password Updated!')
                break

    def getUserCount(self):
        print('Database Class: Data length is ' + str(len(self._data)))