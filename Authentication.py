
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from Helpers import DateHelper

def authenticate(inputPassword, expectedPassword):

    if(inputPassword == expectedPassword):
        print('Authentication Module: Validated!')
        return True
    else:
        print('Authentication Module: Not Validated.')
        return False


def generateJWT(user_name, role):
    token = jwt.encode({'user_id' : user_name, 'role': role, 'exp' : DateHelper.getTokenExpiration()}, "Secret_key", algorithm="HS256")
    return token

def isTokenValid(token, currentUser):
    
    try:
        tokenPayload = jwt.decode(token, 'Secret_key', algorithms=["HS256"])
    except:
        print('Authentication Module: Token has expired.')
        return False
    
    if not tokenPayload:
        print('Authentication Module: Token is null.')
        return False
    
    tokenUser = tokenPayload['user']
    
    #check User
    print('Authentication Module: Current User = ' + currentUser)
    if currentUser != tokenUser:
        print('Authentication Module: Token User does not match current User.')
        return False
    
    return True