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
    response = make_response(Controller.auth(request.json['userName'], request.json['password']))
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

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
@app.route('/user/<currentUserId>/<userId>', methods=['GET'])
def get_user(currentUserId, userId):
    token = request.headers['x-access-token']
    return Controller.getUser(token, currentUserId, userId)

# Create a New User
@app.route('/user/<currentUserId>', methods=['POST'])
def create_user(currentUserId):
    token = request.headers['x-access-token']
    return Controller.createNewUser(token, currentUserId, request.json['firstName'], request.json['lastName'], request.json['age'])

# Deactivate User
@app.route('/user/<currentUserId>/<userId>', methods=['DELETE'])
def deactivate_user(currentUserId, userId):
    token = request.headers['x-access-token']
    return Controller.deactivateUser(token, currentUserId, userId)

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
    print('Main: Event Name = ' + request.json['name'])
    print('Main: Event Location = ' + request.json['location'])
    print('Main: Event Date = ' + request.json['date'])
    return Controller.createNewEvent(token, currentUserId, request.json['name'], request.json['date'], request.json['location'])

# Cancel Event
@app.route('/events/cancel/<currentUserId>', methods=['GET'])
def cancel_event(currentUserId):
    token = request.headers['x-access-token']
    eventId = request.args.get('eventId')
    return Controller.cancelEvent(token, currentUserId, eventId)

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
    return Controller.requestEvent(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

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
@app.route('/events/remove<currentUserId>', methods=['GET'])
def remove_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.removePerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))


if __name__ == '__main__':
    app.run(port=8085)