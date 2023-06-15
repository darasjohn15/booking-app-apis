from flask import *
import Controller

app = Flask(__name__)

# =======================================================================
#  
# Users APIs
#
# ======================================================================= 

# Get All Users
@app.route('/users', methods=['GET'])
def get_all_users():
    return Controller.getUsers()

# Get A Single User by UserID
@app.route('/user', methods=['GET'])
def get_user():
    id = str(request.args.get('userId'))
    return Controller.getUser(id)

# Create a New User
@app.route('/user', methods=['POST'])
def create_user():
    return Controller.createNewUser(request.json['firstName'], request.json['lastName'], request.json['age'])

# Deactivate User
@app.route('/user', methods=['DELETE'])
def deactivate_user():
    return Controller.deactivateUser(request.json['userId'])

# =======================================================================
#  
# Events APIs
#
# ======================================================================= 

# Get All Events
@app.route('/events', methods=['GET'])
def get_all_events():
    return Controller.getEvents()

# Get Events By Location
@app.route('/events/location', methods=['GET'])
def get_events_by_location():
    location = str(request.args.get('location'))
    return Controller.getEventsByLocation(location)

# Get Events By Host
@app.route('/events/host', methods=['GET'])
def get_events_by_host():
    host = str(request.args.get('host'))
    return Controller.getEventsByHost(host)

# Get Events By Date
@app.route('/events/date', methods=['GET'])
def get_events_by_date():
    month = str(request.args.get('month'))
    year = str(request.args.get('year'))
    return Controller.getEventsByDate(month, year)

# Get Events By Venue

# Create New Event 
@app.route('/event', methods=['POST'])
def create_event():
    return Controller.createNewEvent(request.json['name'], request.json['date'], request.json['hostID'], request.json['location'])

# Cancel Event
@app.route('/event/cancel', methods=['GET'])
def cancel_event():
    return Controller.cancelEvent(request.args.get('eventId'))

# Get Performers
@app.route('/event/performers', methods=['GET'])
def get_event_performers():
    return Controller.getEventPerformers(request.args.get('eventId'))

# Get Requested Performers
@app.route('/event/requested', methods=['GET'])
def get_event_requested_performers():
    return Controller.getEventRequestedPerformers(request.args.get('eventId'))

# Add Requested Performer
@app.route('/event/request', methods=['GET'])
def request_performer():
    return Controller.requestEvent(request.args.get('eventId'), request.args.get('userId'))

# Book a Performer
@app.route('/event/approve', methods=['GET'])
def approve_performer():
    return Controller.approvePerformer(request.args.get('eventId'), request.args.get('userId'))

# Deny a Performer
@app.route('/event/deny', methods=['GET'])
def deny_performer():
    return Controller.denyPerformer(request.args.get('eventId'), request.args.get('userId'))

# Remove a Performer from Event
@app.route('/event/remove', methods=['GET'])
def remove_performer():
    return Controller.removePerformer(request.args.get('eventId'), request.args.get('userId'))


if __name__ == '__main__':
    app.run(port=8085)