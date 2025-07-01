import Models.User
import DAL.UsersDAL 
import DAL.VenuesDAL
from flask import *
import Authentication
from DAL import ApplicationsDAL
from DAL import EventsDAL
from dotenv import load_dotenv
import os


load_dotenv() 

# Get the Users Data
users_data = DAL.UsersDAL.UsersDAL("UsersData.json")

#Load Venues Data
venues_data = DAL.VenuesDAL.VenuesDAL("VenuesData.json")

def login_user(request_body):
    #Get request values
    requestEmail = request_body['email']
    requestPassword = request_body['password']

    #Get user data based on userName
    user = users_data.getUserByEmail(requestEmail)

    if not user:
        return jsonify({'message' : 'User not found'}), 401
    
    if Authentication.authenticate(requestPassword, user['password']):
        token = Authentication.generateJWT(user['id'], user['role'])
        return jsonify({
            'token': token,
            'user': {
                'user_id': user['id'],
                'role': user['role'],
                'email': user['email'],
                'name': user.get('name')
            }
        }), 200

    return jsonify({'message' : 'Invalid Login' }), 401

def get_user(userId):
    data_set = users_data.get_user(userId)
    return jsonify(data_set), 200

def create_user(requestBody):
    required_fields = ["firstName", "lastName", "email", "userName", "password", "age"]

    # Validate all required fields
    for field in required_fields:
        if field not in requestBody or requestBody[field] in [None, ""]:
            return jsonify({'error': f'Missing or empty required field: {field}'}), 400

    # Additional validation (e.g. age should be int and > 0)
    try:
        age = int(requestBody['age'])
        if age <= 0:
            return jsonify({'error': 'Age must be a positive number'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Age must be a valid integer'}), 400
    
    #Get Request Values
    firstName = requestBody['firstName']
    lastName = requestBody['lastName']
    email = requestBody['email']
    userName = requestBody['userName']
    password = requestBody['password']
    age = requestBody['age']

    #Create User
    newUser = Models.User.User(firstName, lastName, email, userName, password, age)
    
    #Save New User to Database
    users_data.addUser(newUser)

    return jsonify({"userName": newUser.userName, "password": newUser.password}), 200


def get_events(host_id, active, location):
    # convert 'true'/'false' strings to boolean if needed
    if active is not None:
        active = active.lower() == 'true'

    events = DAL.EventsDAL.get_events(host_id, active, location)

    return events

def get_event(event_id):
    event = DAL.EventsDAL.get_event(event_id)
    return event

def update_event(event_id, title=None, date=None, venue_id=None, description=None, is_active=None):
    updated_event = EventsDAL.update_event(
        event_id,
        title,
        date,
        venue_id,
        description,
        is_active
    )
    return updated_event

def create_event(host_id, venue_id, title, description, location, date):
    return DAL.EventsDAL.create_event(host_id, venue_id, title, description, location, date)

def get_applications(event_id, performer_id, status):
    applications = DAL.ApplicationsDAL.get_applications(event_id, performer_id, status)
    return applications

def get_application(application_id):
    event = DAL.ApplicationsDAL.get_application(application_id)
    return event
    
def create_application(event_id, performer_id):
     return DAL.ApplicationsDAL.create_application(event_id, performer_id)

def update_application(application_id, status):
    updated_application = ApplicationsDAL.update_application(application_id, status)
    return updated_application

def get_venues():
    results = venues_data.get_venues()
    return jsonify(results), 200





