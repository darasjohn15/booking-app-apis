
import jwt
import datetime

def authenticate(inputPassword, expectedPassword):

    if(inputPassword == expectedPassword):
        print('Authentication Module: Validated!')
        return True
    else:
        print('Authentication Module: Not Validated.')
        return False


def generateJWT(userName):
    token = jwt.encode({'user' : userName, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, "Secret_key", algorithm="HS256")
    return token