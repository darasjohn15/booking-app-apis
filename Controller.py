import DAL.VenuesDAL
from flask import *
import auth_utils
from DAL import ApplicationsDAL
from DAL import events_dal
from DAL import users_dal
from helpers import password_helper
from dotenv import load_dotenv
import os

load_dotenv() 

#Load Venues Data
venues_data = DAL.VenuesDAL.VenuesDAL("VenuesData.json")

def login(email, password):
    users = get_users(None, email, None, None)
    
    if not users:
        return jsonify({'message' : 'User not found'}), 401
    
    user = users[0]
    
    if password_helper.verify_password(password, user['password_hash']):
        token = auth_utils.generate_jwt(user['id'], user['role'])
        return {
            'token': token,
            'user': {
                'user_id': user['id'],
                'role': user['role'],
                'email': user['email'],
                'name': user.get('name')
            }
        }

    return None

def get_user(userId):
    user = users_dal.get_user(userId)
    return user

def get_users(name, email, role, active):
    # convert 'true'/'false' strings to boolean if needed
    if active is not None:
        active = active.lower() == 'true'

    users = users_dal.get_users(name, email, role, active)

    return users

def create_user(name, email, password, role):
    if password:
        password = password_helper.hash_password(password)

    return users_dal.create_user(name, email, password, role)

def update_user(user_id, name=None, email=None, password=None, role=None):
    if password:
        password = password_helper.hash_password(password)

    updated_user = users_dal.update_user(user_id, name, email, password, role)
    return updated_user

def get_events(host_id, active, location):
    # convert 'true'/'false' strings to boolean if needed
    if active is not None:
        active = active.lower() == 'true'

    events = events_dal.get_events(host_id, active, location)

    return events

def get_event(event_id):
    event = events_dal.get_event(event_id)
    return event

def update_event(event_id, title=None, date=None, venue_id=None, description=None, is_active=None):
    updated_event = events_dal.update_event(
        event_id,
        title,
        date,
        venue_id,
        description,
        is_active
    )
    return updated_event

def create_event(host_id, venue_id, title, description, location, date):
    return events_dal.create_event(host_id, venue_id, title, description, location, date)

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





