from flask import *
from flask_cors import CORS
import Controller

app = Flask(__name__)
CORS(app)

# =======================================================================
#  
# Authentication API
#
# ======================================================================= 

@app.route('/login', methods=['POST'])
def login():
    return Controller.auth(request.json)

# =======================================================================
#  
# Users APIs
#
# ======================================================================= 

# Get All Users
@app.route('/users/<currentUserId>', methods=['GET'])
def get_all_users(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getUsers(token, currentUserId)

# Get A Single User by UserID
@app.route('/users/<currentUserId>/<userId>', methods=['GET'])
def get_user(currentUserId, userId):
    token = request.headers['x-access-token']
    return Controller.getUser(token, currentUserId, userId)

# Create a New User
@app.route('/users', methods=['POST'])
def create_user():
    return Controller.createNewUser(request.json)

# Deactivate User
@app.route('/users/<currentUserId>', methods=['DELETE'])
def deactivate_user(currentUserId):
    token = request.headers['x-access-token']
    return Controller.deactivateUser(token, currentUserId)

# Activate User
@app.route('/users/activate/<currentUserId>', methods=['GET'])
def activate_user(currentUserId):
    token = request.headers['x-access-token']
    return Controller.activateUser(token, currentUserId)

# Edit User Info
@app.route('/users/<currentUserId>', methods=['PUT'])
def edit_user_info(currentUserId):
    token = request.headers['x-access-token']
    return Controller.editUserInfo(token, currentUserId, request.json)

# Change User Password
@app.route('/users/password/<currentUserId>', methods=['PUT'])
def change_user_password(currentUserId):
    token = request.headers['x-access-token']
    return Controller.changePassword(token, currentUserId, request.json)

# =======================================================================
#  
# Events APIs
#
# ======================================================================= 

# Get All Events
@app.route('/events/<currentUserId>', methods=['GET'])
def get_all_events(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getEvents(token, currentUserId)

@app.route('/events/active/<currentUserId>', methods=['GET'])
def get_all_active_events(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getActiveEvents(token, currentUserId)

# Get Events By Location
@app.route('/events/location/<currentUserId>', methods=['GET'])
def get_events_by_location(currentUserId):
    location = str(request.args.get('location'))
    token = request.headers['x-access-token']
    return Controller.getEventsByLocation(token, currentUserId, location)

# Get Event Details
@app.route('/events/<currentUserId>/<eventId>', methods=['GET'])
def get_event_details(currentUserId, eventId):
    token = request.headers['x-access-token']
    return Controller.getEvent(token, currentUserId, eventId)

# Get Events By Host
@app.route('/events/host/<currentUserId>', methods=['GET'])
def get_events_by_host(currentUserId):
    host = str(request.args.get('host'))
    token = request.headers['x-access-token']
    return Controller.getEventsByHost(token, currentUserId, host)

# Get Events By Date
@app.route('/events/date/<currentUserId>', methods=['GET'])
def get_events_by_date(currentUserId):
    month = str(request.args.get('month'))
    year = str(request.args.get('year'))
    token = request.headers['x-access-token']
    return Controller.getEventsByDate(token, currentUserId, month, year)

# Get Events By Venue

# Create New Event 
@app.route('/events/<currentUserId>', methods=['POST'])
def create_event(currentUserId):
    token = request.headers['x-access-token']
    return Controller.createNewEvent(token, currentUserId, request.json)

# Cancel Event
@app.route('/events/cancel/<currentUserId>/<eventId>', methods=['GET'])
def cancel_event(currentUserId, eventId):
    token = request.headers['x-access-token']
    return Controller.cancelEvent(token, currentUserId, eventId)

# Activate Event
@app.route('/events/activate/<currentUserId>/<eventId>', methods=['GET'])
def activate_event(currentUserId, eventId):
    token = request.headers['x-access-token']
    return Controller.activateEvent(token, currentUserId, eventId)

# Edit Event Info
@app.route('/events/<currentUserId>/<eventId>', methods=['PUT'])
def edit_event(currentUserId, eventId):
    token = request.headers['x-access-token']
    return Controller.editEvent(token, currentUserId, eventId, request.json)

# Get Performers
@app.route('/events/performers/<currentUserId>', methods=['GET'])
def get_event_performers(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getEventPerformers(token, currentUserId, request.args.get('eventId'))

# Get Requested Performers
@app.route('/events/requested/<currentUserId>', methods=['GET'])
def get_event_requesteds_performers(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getEventRequestedPerformers(token, currentUserId, request.args.get('eventId'))

# Add Requested Performer
@app.route('/events/request/<currentUserId>', methods=['GET'])
def request_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.requestEvent(token, currentUserId, request.args.get('eventId'))

# Book a Performer
@app.route('/events/approve/<currentUserId>', methods=['GET'])
def approve_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.approvePerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

# Deny a Performer
@app.route('/events/deny/<currentUserId>', methods=['GET'])
def deny_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.denyPerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

# Remove a Performer from Event
@app.route('/events/remove/<currentUserId>', methods=['GET'])
def remove_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.removePerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

if __name__ == '__main__':
    app.run(port=8085)