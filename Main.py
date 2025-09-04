from flask import *
from flask_cors import CORS, cross_origin
import controller
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
    credentials = request.json
    results = controller.login(credentials['email'], credentials['password'])
    if results:
        return jsonify(results), 200
    else:
        return jsonify({"message": "Invalid Login."}), 401

# =======================================================================
#  
# Users Endpoints
#
# ======================================================================= 

# Get User
@app.route('/users/<user_id>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_user(user_id):
    user = controller.get_user(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({'error': 'User not found'}), 404
    
# Get Users
@app.route('/users', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_users():
    name = request.args.get('host_id', default=None, type=str)
    email = request.args.get('email', default=None, type=str)
    role = request.args.get('role', default=None, type=str)
    active = request.args.get('active', default=None, type=str)

    users = controller.get_users(name, email, role, active)
    
    return jsonify(users), 200
    
# Create User 
@app.route('/users', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
def create_user():
    data = request.get_json()

    user = controller.create_user(
        name=data['name'],
        email=data['email'],
        password=data['password'],
        role=data['role']
    )

    return jsonify(user), 201

# Update User
@app.route('/users', methods=['PUT'])
@cross_origin(origin='http://localhost:4200')
@token_required
def update_user():
    data = request.get_json()

    id = data.get('id')
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    updated_user = controller.update_user(
        id,
        name,
        email,
        password,
        role
    )

    if updated_user:
        return jsonify(updated_user), 200
    else:
        return jsonify({'error': 'User not found or update failed'}), 404

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

    events = controller.get_events(host_id, active, location)
    
    return jsonify(events), 200

# Create New Event 
@app.route('/events', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def create_event():
    data = request.get_json()

    event = controller.create_event(
        host_id=data['host_id'],
        venue_id=data['venue_id'],
        title=data['title'],
        description=data['description'],
        location=data['location'],
        date=data['date']
    )

    return jsonify(event), 201

# Get an Event
@app.route('/events/<eventId>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_event(eventId):
    event = controller.get_event(eventId)
    if event:
        return jsonify(event)
    else:
        return jsonify({'error': 'Event not found'}), 404

# Update Event
@app.route('/events', methods=['PUT'])
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

    updated_event = controller.update_event(
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
    
# Get Event Performers
@app.route('/events/performers/<event_id>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_event_performers(event_id):
    performers = controller.get_event_performers(event_id)
    return jsonify(performers), 200


# =======================================================================
#  
# Applications Endpoints
#
# ======================================================================= 

# Get Applications
@app.route('/applications', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_applications():
    event_id = request.args.get('event_id', default=None, type=int)
    performer_id = request.args.get('performer_id', default=None, type=str)
    status = request.args.get('status', default=None, type=str)

    applications = controller.get_applications(event_id, performer_id, status)
    
    if applications:
        return jsonify(applications), 200
    else:
        return jsonify({'message': 'No events found'}), 404

# Create Application
@app.route('/applications', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def create_application():
    data = request.get_json()

    application = controller.create_application(
        event_id=data['event_id'],
        performer_id=data['performer_id']
    )

    return jsonify(application), 201

# Update Application
@app.route('/applications', methods=['PUT'])
@cross_origin(origin='http://localhost:4200')
@token_required
def update_application():
    data = request.get_json()

    id = data.get('id')
    status = data.get('status')

    updated_application = controller.update_application(
        id,
        status
    )

    if updated_application:
        return jsonify(updated_application), 200
    else:
        return jsonify({'error': 'Application not found or update failed'}), 404

# Get an Application
@app.route('/applications/<application_id>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_application(application_id):
    application = controller.get_application(application_id)

    if application:
        return jsonify(application)
    else:
        return jsonify({'error': 'Application not found'}), 404

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
    return controller.get_venues()

if __name__ == '__main__':
    app.run(port=8085)