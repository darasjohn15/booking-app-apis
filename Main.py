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

# Get All Events
@app.route('/events', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_events():
    return Controller.get_events()

# Create New Event 
@app.route('/events', methods=['POST'])
@cross_origin(origin='http://localhost:4200')
@token_required
def create_event():
    request_body = request.json
    return Controller.create_event(request_body)

# Get Event
@app.route('/events/<eventId>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_event(eventId):
    return Controller.get_event(eventId)

# Get Events By Host
@app.route('/events/host/<host_id>', methods=['GET'])
@cross_origin(origin='http://localhost:4200')
@token_required
def get_events_by_host(host_id):
    return Controller.get_events_by_host(host_id)

# Update Event
@app.route('/events/update', methods=['PUT'])
@cross_origin(origin='http://localhost:4200')
@token_required
def update_event():
    return Controller.update_event(request.json)

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