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

## API Testing
Use the included Postman collection to test the API:

- File: `booking-app-api.postman_collection.json`
- Import it into Postman and set the base URL (e.g., `https://booking-app-apis.onrender.com`)

## API Endpoints

> All authenticated endpoints require a `Bearer <token>` in the `Authorization` header.

---

### Auth

| Method | Endpoint     | Description                     |
|--------|--------------|---------------------------------|
| POST   | `/login`     | User login and JWT token retrieval |

---

### Users

| Method | Endpoint        | Description          |
|--------|------------------|----------------------|
| GET    | `/users/:userId` | Get a user by ID     |

---

### Events

| Method | Endpoint                   | Description                        |
|--------|-----------------------------|------------------------------------|
| GET    | `/events`                   | Get all events                     |
| GET    | `/events/:eventId`          | Get a specific event by ID         |
| GET    | `/events/host/:hostId`      | Get events hosted by a specific host |
| POST   | `/events`                   | Create a new event                 |
| PUT    | `/events/:userId/:eventId`  | Update an event *(legacy/test)*   |

---

### Applications

| Method | Endpoint                                            | Description                         |
|--------|------------------------------------------------------|-------------------------------------|
| GET    | `/events/applications/:eventId`                      | Get all applications for an event   |
| GET    | `/events/applications/performer/:performerId`        | Get all applications by a performer |
| POST   | `/events/applications`                               | Submit an application to an event   |
| POST   | `/events/applications/approve`                       | Approve an application              |
| POST   | `/events/applications/deny`                          | Deny an application                 |

---

### Venues

| Method | Endpoint     | Description         |
|--------|--------------|---------------------|
| GET    | `/venues`    | Get a list of venues |

## Status
Actively in development. Designed for local testing and API prototyping — easily extendable to support persistent storage and production use.
