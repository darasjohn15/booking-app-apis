from flask import *
import auth_utils
from dal import applications_dal
from dal import events_dal
from dal import users_dal
from dal import venues_dal
from helpers import password_helper
from dotenv import load_dotenv
import os

load_dotenv() 

def login(email, password):
    users = get_users(None, email, None, True)
    
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

def get_events(host_id, active, location, venue_id, date_start, date_end, page_number):
    # convert 'true'/'false' strings to boolean if needed
    if active is not None:
        active = active.lower() == 'true'

    events = events_dal.get_events(host_id, active, location, venue_id, date_start, date_end, page_number)

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

def create_event(host_id, venue_id, title, description, date):
    return events_dal.create_event(host_id, venue_id, title, description, date)

def get_event_performers(event_id):
    applications = applications_dal.get_applications(event_id, None, None)
    approved_apps = [app for app in applications if app["status"] == "approved"]
    
    performers = []
    for app in approved_apps:
        performer_id = app["performer_id"]
        user = users_dal.get_user(performer_id)
        performers.append(user)

    return performers

def get_applications(event_id, performer_id, status):
    applications = applications_dal.get_applications(event_id, performer_id, status)
    return applications

def get_application(application_id):
    event = applications_dal.get_application(application_id)
    return event
    
def create_application(event_id, performer_id):
     return applications_dal.create_application(event_id, performer_id)

def update_application(application_id, status):
    updated_application = applications_dal.update_application(application_id, status)
    return updated_application

def get_venue(venue_id):
    venue = venues_dal.get_venue(venue_id)
    return venue

def get_venues():
    venues = venues_dal.get_venues()
    return venues