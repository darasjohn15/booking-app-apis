class Authentication:
    def __init__(self):
        pass

    def authenticate(self, data, userName, password):
        for x in data:
            if(userName == x['_userName'] and x['_active'] == True ):
                if(password == x['_password']):
                    self.currentUser = x
                    print('')
                    return True
                else:
                    print('Incorret password for ' + x['_userName'])
                    return False
            else:
                continue

        print('')
        print('Invalid Username.')
        print('')
        
        return False