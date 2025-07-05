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
**Storage**: PostgreSQL Database 
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
| GET    | `/users`         | Get a list of users by ID. Supports query parameters     |
| GET    | `/users/:userId` | Get a user by ID     |
| POST   | `/users`         | Create a user     |
| PUT    | `/users`         | Edit a user by ID     |

---

### Events

| Method | Endpoint                    | Description                        |
|--------|-----------------------------|------------------------------------|
| GET    | `/events`                   | Get a list of events. Supports query parameters  |
| GET    | `/events/:eventId`          | Get an event by ID         |
| POST   | `/events`                   | Create a event                 |
| PUT    | `/events`                   | Edit an event   |

---

### Applications

| Method | Endpoint                                              | Description                         |
|--------|------------------------------------------------------|-------------------------------------|
| GET    | `/applications`                      | Get a list of applications. Supports query parameters   |
| GET    | `/applications/:applicatonId`        | Get an applications by ID |
| POST   | `/applications`                      | Create an application  |
| PUT    | `/applications`                      | Update an application status |

---

### Venues

| Method | Endpoint     | Description         |
|--------|--------------|---------------------|
| GET    | `/venues`    | Get a list of venues |
