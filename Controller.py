import Models.User
import Models.Event
import Models.Message
import Models.Application
import DAL.UsersDAL 
import DAL.EventsDAL
import DAL.VenuesDAL
from flask import *
import Authentication
from db import get_db_connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os


load_dotenv() 

# Get the Users Data
users_data = DAL.UsersDAL.UsersDAL("UsersData.json")

#Get Events Data
events_data = DAL.EventsDAL.EventsDAL("EventsData.json")

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
    updated_event = DAL.EventsDAL.update_event(
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

def get_applications(event_id):
    event = events_data.get_event(event_id)
    applications = event['applications']
    return jsonify(applications), 200

def get_performer_applications(performer_id):
    results = []

    events = events_data.get_events()
    
    for event in events:
        applications = event['applications']
        for application in applications:
            if (application['performer_id'] == performer_id):
                results.append(application)
    
    return jsonify(results), 200
    
def add_application(request_body):
     event_id = request_body['eventID']
     performer_id = request_body['performerID']

     event = events_data.get_event(event_id)
     event_title = event['title']
     performer = users_data.get_user(performer_id)
     performer_name = performer['name']

     new_application = Models.Application.Application(event_id, event_title, performer_id, performer_name)

     events_data.add_application(event_id, new_application)

     return jsonify({'message': "Application Submitted!"}), 200

def approve_application(request_body):
    event_id = request_body['eventID']
    application_id = request_body['applicationID']

    event = events_data.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    for app in event['applications']:
        if app['id'] == application_id:
            app['status'] = 'approved'
            event['performers'].append(app['performer_id'])
            events_data.save()
            return jsonify({'message': 'Application approved'}), 200

    return jsonify({'message': 'Application not found'}), 404

def deny_application(request_body):
    event_id = request_body['eventID']
    application_id = request_body['applicationID']

    event = events_data.get_event(event_id)
    if not event:
        return jsonify({'message': 'Event not found'}), 404

    for app in event['applications']:
        if app['id'] == application_id:
            app['status'] = 'denied'
            events_data.save()
            return jsonify({'message': 'Application denied'}), 200

    return jsonify({'message': 'Application not found'}), 404

def get_venues():
    results = venues_data.get_venues()
    return jsonify(results), 200





