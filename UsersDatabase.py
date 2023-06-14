import Database

class UsersDatabase(Database.Database):

    def addUser(self, user):
        self._data.append(user)
        self.save()
        self.reload()
        print('')
        print('New User Created!')
        print('')

    def getUsers(self):
        return self._data

    def getUser(self, id):
        for x in self._data:
            userid = x['id']
            if(id == userid):
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

    def getUserCount(self):
        print('Database Class: Data length is ' + str(len(self._data)))