from flask import *
import Controller

app = Flask(__name__)

# =======================================================================
#  
# Authentication API
#
# ======================================================================= 

@app.route('/login', methods=['POST'])
def login():
    return Controller.auth(request.json['userName'], request.json['password'])

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
@app.route('/event/<currentUserId>', methods=['POST'])
def create_event(currentUserId):
    token = request.headers['x-access-token']
    return Controller.createNewEvent(token, currentUserId, request.json['name'], request.json['date'], request.json['hostID'], request.json['location'])

# Cancel Event
@app.route('/event/cancel/<currentUserId>', methods=['GET'])
def cancel_event(currentUserId):
    token = request.headers['x-access-token']
    return Controller.cancelEvent(token, currentUserId, request.args.get('eventId'))

# Get Performers
@app.route('/event/performers/<currentUserId>', methods=['GET'])
def get_event_performers(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getEventPerformers(token, currentUserId, request.args.get('eventId'))

# Get Requested Performers
@app.route('/event/requested/<currentUserId>', methods=['GET'])
def get_event_requested_performers(currentUserId):
    token = request.headers['x-access-token']
    return Controller.getEventRequestedPerformers(token, currentUserId, request.args.get('eventId'))

# Add Requested Performer
@app.route('/event/request/<currentUserId>', methods=['GET'])
def request_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.requestEvent(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

# Book a Performer
@app.route('/event/approve/<currentUserId>', methods=['GET'])
def approve_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.approvePerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

# Deny a Performer
@app.route('/event/deny/<currentUserId>', methods=['GET'])
def deny_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.denyPerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))

# Remove a Performer from Event
@app.route('/event/remove<currentUserId>', methods=['GET'])
def remove_performer(currentUserId):
    token = request.headers['x-access-token']
    return Controller.removePerformer(token, currentUserId, request.args.get('eventId'), request.args.get('userId'))


if __name__ == '__main__':
    app.run(port=8085)