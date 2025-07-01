import DAL.VenuesDAL
from flask import *
import Authentication
from DAL import ApplicationsDAL
from DAL import EventsDAL
from DAL import UsersDAL
from helpers import password_helper
from dotenv import load_dotenv
import os

load_dotenv() 

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
    user = UsersDAL.get_user(userId)
    return user

def create_user(name, email, password, role):
    if password:
        password = password_helper.hash_password(password)

    return UsersDAL.create_user(name, email, password, role)

def update_user(user_id, name=None, email=None, password=None, role=None):
    if password:
        password = password_helper.hash_password(password)

    updated_user = UsersDAL.update_user(user_id, name, email, password, role)
    return updated_user

def get_events(host_id, active, location):
    # convert 'true'/'false' strings to boolean if needed
    if active is not None:
        active = active.lower() == 'true'

    events = EventsDAL.get_events(host_id, active, location)

    return events

def get_event(event_id):
    event = EventsDAL.get_event(event_id)
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
    return EventsDAL.create_event(host_id, venue_id, title, description, location, date)

def get_applications(event_id, performer_id, status):
    applications = ApplicationsDAL.get_applications(event_id, performer_id, status)
    return applications

def get_application(application_id):
    event = ApplicationsDAL.get_application(application_id)
    return event
    
def create_application(event_id, performer_id):
     return ApplicationsDAL.create_application(event_id, performer_id)

def update_application(application_id, status):
    updated_application = ApplicationsDAL.update_application(application_id, status)
    return updated_application

def get_venues():
    results = venues_data.get_venues()
    return jsonify(results), 200





