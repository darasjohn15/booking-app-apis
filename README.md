# Performer Booking API
This is the backend service for the Performer Booking App, a platform that connects performers with venue owners to simplify event booking and management. The API handles user authentication, event data, application workflows, and role-based access control.

## Features
**User Management**  
Handles login, registration, and role distinction (host vs. performer)

**Event Management**  
Hosts can create and manage events, each tied to a venue and location

**Performer Applications**  
Performers can apply to events; hosts can review and approve/deny applications

**Secure Endpoints**  
Protected routes with token validation and custom role-based access

**Data Storage**  
Lightweight local file-based data storage (JSON) for quick testing and prototyping

## Tech Stack
**Language**: Python 3  
**Framework**: Flask  
**Storage**: JSON files  
**Authentication**: JWT-based auth

## Getting Started
```
# Clone the repo
git clone https://github.com/darasjohn15/booking-app-api.git
cd booking-app-api

# (Optional) Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py

# Server runs on http://127.0.0.1:4200 by default.
```

## Project Structure
```
booking-app-api/

├── DAL/               # Data Access Layer files
├── Data/              # Local JSON data files
├── Helpers/           # Helpers
├── Models/            # Data models
├── auth_utils/        # Authentication utilities
├── Authentication.py  # Misc utilities (e.g., validators)
├── Controller.py      # Request handler
└── Main.py            # Main app entry point
```

## Sample Endpoints  
* ```POST /login```
* ```POST /register```
* ```GET /events```
* ```POST /apply```
* ```GET /applications```
* ```POST /applications/approve```

## API Testing
Use the included Postman collection to test the API:

- File: `booking-app-api.postman_collection.json`
- Import it into Postman and set the base URL (e.g., `https://booking-app-apis.onrender.com`)

## Status
Actively in development. Designed for local testing and API prototyping — easily extendable to support persistent storage and production use.
