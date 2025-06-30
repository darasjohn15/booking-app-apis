from flask import *
from flask_cors import CORS, cross_origin
import Controller
from auth_utils import token_required

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
    "https://booking-web-app-asce.onrender.com"
]}}, supports_credentials=True)

# =======================================================================
#  
# Authentication Endpoints
#
# ======================================================================= 

@app.route('/login', methods=['POST'])
def login():
    return Controller.login_user(request.json)

# =======================================================================
#  
# Users Endpoints
#
# ======================================================================= 

# Get A Single User by UserID
@app.route('/users/<userId>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_user(userId):
    return Controller.get_user(userId)

# =======================================================================
#  
# Events Endpoints
#
# ======================================================================= 

# Get Events
@app.route('/events', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_events():
    host_id = request.args.get('host_id', default=None, type=int)
    active = request.args.get('active', default=None, type=str)
    location = request.args.get('location', default=None, type=str)

    events = Controller.get_events(host_id, active, location)
    
    if events:
        return jsonify(events), 200
    else:
        return jsonify({'message': 'No events found'}), 404

# Create New Event 
@app.route('/events', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def create_event():
    data = request.get_json()

    event = Controller.create_event(
        host_id=data['host_id'],
        venue_id=data['venue_id'],
        title=data['title'],
        description=data['description'],
        location=data['location'],
        date=data['date']
    )

    return jsonify(event), 201

# Get Event
@app.route('/events/<eventId>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_event(eventId):
    event = Controller.get_event(eventId)
    if event:
        return jsonify(event)
    else:
        return jsonify({'error': 'Event not found'}), 404

# Update Event
@app.route('/events/update', methods=['PUT'])
@cross_origin(origin='http://localhost:4200')
@token_required
def update_event():
    data = request.get_json()

    id = data.get('id')
    title = data.get('title')
    date = data.get('date')
    venue_id = data.get('venue_id')
    description = data.get('description')
    is_active = data.get('is_active')

    updated_event = Controller.update_event(
        id,
        title,
        date,
        venue_id,
        description,
        is_active
    )

    if updated_event:
        return jsonify(updated_event), 200
    else:
        return jsonify({'error': 'Event not found or update failed'}), 404

# Get Applications
@app.route('/events/applications/<event_id>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_applications(event_id):
    return Controller.get_applications(event_id)

# Get Performer Applications
@app.route('/events/applications/performer/<performer_id>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_performer_applications(performer_id):
    return Controller.get_performer_applications(performer_id)

# Add Application
@app.route('/events/applications', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def add_application():
    request_body = request.json
    return Controller.add_application(request_body)

# Approve an Application
@app.route('/events/applications/approve', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def approve_application():
    return Controller.approve_application(request.json)

# Deny an Application
@app.route('/events/applications/deny', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def deny_performer():
    return Controller.deny_application(request.json)

# =======================================================================
#  
# Venues Endpoints
#
# ======================================================================= 

# Get Venues
@app.route('/venues', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_venues():
    return Controller.get_venues()

if __name__ == '__main__':
    app.run(port=8085)