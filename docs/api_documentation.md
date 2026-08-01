# API Documentation

This document describes the available REST API endpoints for the Performer Booking API.

## Base URL

Use your local or deployed API URL as the base URL.

```text
http://127.0.0.1:8085
```

## Authentication

Most endpoints require a JWT token in the `Authorization` header.

```http
Authorization: Bearer <token>
```

Get a token by logging in with `POST /login`.

If a protected endpoint is called without a valid token, the API returns `401`.

## Endpoint Summary

| Method | Endpoint                         | Auth Required | Description |
| ------ | -------------------------------- | ------------- | ----------- |
| GET    | `/ping`                          | No            | Health check endpoint. |
| POST   | `/login`                         | No            | Log in and receive a JWT token. |
| GET    | `/users`                         | Yes           | Get users with optional filters. |
| GET    | `/users/<user_id>`               | Yes           | Get one user by ID. |
| POST   | `/users`                         | No            | Create a new user. |
| PUT    | `/users`                         | Yes           | Update an existing user. |
| PUT    | `/users/change-password`         | Yes           | Change a user's password. |
| GET    | `/events`                        | Yes           | Get events with optional filters and pagination. |
| GET    | `/events/<event_id>`             | Yes           | Get one event by ID. |
| POST   | `/events`                        | Yes           | Create a new event. |
| PUT    | `/events`                        | Yes           | Update an existing event. |
| GET    | `/events/performers/<event_id>`  | Yes           | Get approved performers for an event. |
| GET    | `/applications`                  | Yes           | Get applications with optional filters. |
| GET    | `/applications/<application_id>` | Yes           | Get one application by ID. |
| POST   | `/applications`                  | Yes           | Create a performer application. |
| PUT    | `/applications`                  | Yes           | Update an application status. |
| GET    | `/venues`                        | Yes           | Get all venues. |

## Health Check

### GET `/ping`

Checks whether the API is running.

#### Response

```json
{
  "status": "Ok"
}
```

## Authentication Endpoints

### POST `/login`

Logs in a user and returns a JWT token.

#### Request Body

```json
{
  "email": "host@example.com",
  "password": "password123"
}
```

#### Success Response

Status: `200`

```json
{
  "token": "<jwt-token>",
  "user": {
    "user_id": 1,
    "role": "host",
    "email": "host@example.com",
    "name": "Host User"
  }
}
```

#### Error Response

Status: `401`

```json
{
  "message": "Invalid Login."
}
```

## Users

### GET `/users`

Returns a list of users. Supports optional filters.

#### Query Parameters

| Parameter | Type   | Required | Description |
| --------- | ------ | -------- | ----------- |
| `host_id` | string | No       | Filters users by name in the current implementation. |
| `email`   | string | No       | Filters users by email. |
| `role`    | string | No       | Filters users by role, such as `host` or `performer`. |
| `active`  | string | No       | Filters users by active status, such as `true` or `false`. |

#### Example

```http
GET /users?email=host@example.com&role=host&active=true
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
[
  {
    "id": 1,
    "name": "Host User",
    "email": "host@example.com",
    "password_hash": "<hashed-password>",
    "role": "host",
    "is_active": true,
    "created_at": "2026-01-15T12:00:00"
  }
]
```

### GET `/users/<user_id>`

Returns one user by ID.

#### Example

```http
GET /users/1
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
{
  "id": 1,
  "name": "Host User",
  "email": "host@example.com",
  "password_hash": "<hashed-password>",
  "role": "host",
  "is_active": true,
  "created_at": "2026-01-15T12:00:00"
}
```

#### Error Response

Status: `404`

```json
{
  "error": "User not found"
}
```

### POST `/users`

Creates a new user account.

#### Request Body

```json
{
  "name": "Performer User",
  "email": "performer@example.com",
  "password": "password123",
  "role": "performer"
}
```

#### Success Response

Status: `201`

```json
{
  "id": 2,
  "name": "Performer User",
  "email": "performer@example.com",
  "password_hash": "<hashed-password>",
  "role": "performer",
  "is_active": true,
  "created_at": "2026-01-15T12:00:00"
}
```

### PUT `/users`

Updates an existing user. Only include fields that should be changed.

#### Request Body

```json
{
  "id": 2,
  "name": "Updated Performer",
  "email": "updated.performer@example.com",
  "password": "new-password123",
  "role": "performer",
  "is_active": true
}
```

#### Success Response

Status: `200`

```json
{
  "id": 2,
  "name": "Updated Performer",
  "email": "updated.performer@example.com",
  "password_hash": "<hashed-password>",
  "role": "performer",
  "is_active": true,
  "created_at": "2026-01-15T12:00:00"
}
```

#### Error Response

Status: `404`

```json
{
  "error": "User not found or update failed"
}
```

### PUT `/users/change-password`

Changes a user's password after validating the current password.

#### Request Body

```json
{
  "user_id": 2,
  "current_password": "password123",
  "new_password": "new-password123"
}
```

#### Success Response

Status: `200`

Returns the updated user.

#### Error Response

Status: `400`

```json
{
  "error": "Current password is incorrect"
}
```

Possible error messages include `User not found` and `Current password is incorrect`.

## Events

### GET `/events`

Returns a list of events. Supports optional filters and pagination.

#### Query Parameters

| Parameter     | Type    | Required | Description |
| ------------- | ------- | -------- | ----------- |
| `host_id`     | integer | No       | Filters events by host user ID. |
| `active`      | string  | No       | Filters events by active status. Use `true` or `false`. |
| `location`    | string  | No       | Filters events by location. |
| `venue_id`    | integer | No       | Filters events by venue ID. |
| `date_start`  | string  | No       | Filters events on or after this date. |
| `date_end`    | string  | No       | Filters events on or before this date. |
| `page_number` | integer | No       | Page number for pagination. The page size is 6. |

#### Example

```http
GET /events?host_id=1&active=true&venue_id=2&page_number=1
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
[
  {
    "id": 1,
    "host_id": 1,
    "venue_id": 2,
    "title": "Friday Night Showcase",
    "description": "Live performance event.",
    "location": "Atlanta",
    "date": "2026-03-01T19:00:00",
    "created_at": "2026-01-15T12:00:00",
    "is_active": true,
    "total_count": 1
  }
]
```

### GET `/events/<event_id>`

Returns one event by ID.

#### Example

```http
GET /events/1
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
{
  "id": 1,
  "host_id": 1,
  "title": "Friday Night Showcase",
  "description": "Live performance event.",
  "location": "Atlanta",
  "date": "2026-03-01T19:00:00",
  "created_at": "2026-01-15T12:00:00"
}
```

#### Error Response

Status: `404`

```json
{
  "error": "Event not found"
}
```

### POST `/events`

Creates a new event.

#### Request Body

```json
{
  "hostID": 1,
  "venueID": 2,
  "title": "Friday Night Showcase",
  "description": "Live performance event.",
  "date": "2026-03-01T19:00:00"
}
```

#### Success Response

Status: `201`

```json
{
  "id": 1,
  "host_id": 1,
  "venue_id": 2,
  "title": "Friday Night Showcase",
  "description": "Live performance event.",
  "date": "2026-03-01T19:00:00",
  "created_at": "2026-01-15T12:00:00",
  "is_active": true
}
```

### PUT `/events`

Updates an existing event. Only include fields that should be changed.

#### Request Body

```json
{
  "id": 1,
  "title": "Updated Showcase",
  "date": "2026-03-02T19:00:00",
  "venue_id": 3,
  "description": "Updated event description.",
  "is_active": true
}
```

#### Success Response

Status: `200`

```json
{
  "id": 1,
  "host_id": 1,
  "venue_id": 3,
  "title": "Updated Showcase",
  "description": "Updated event description.",
  "location": "Atlanta",
  "date": "2026-03-02T19:00:00",
  "created_at": "2026-01-15T12:00:00",
  "is_active": true
}
```

#### Error Response

Status: `404`

```json
{
  "error": "Event not found or update failed"
}
```

### GET `/events/performers/<event_id>`

Returns users who have approved applications for the selected event.

#### Example

```http
GET /events/performers/1
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
[
  {
    "id": 2,
    "name": "Performer User",
    "email": "performer@example.com",
    "password_hash": "<hashed-password>",
    "role": "performer",
    "is_active": true,
    "created_at": "2026-01-15T12:00:00"
  }
]
```

## Applications

### GET `/applications`

Returns performer applications. Supports optional filters.

#### Query Parameters

| Parameter      | Type    | Required | Description |
| -------------- | ------- | -------- | ----------- |
| `event_id`     | integer | No       | Filters applications by event ID. |
| `performer_id` | string  | No       | Filters applications by performer user ID. |
| `status`       | string  | No       | Filters applications by status, such as `pending`, `approved`, or `denied`. |

#### Example

```http
GET /applications?event_id=1&status=pending
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
[
  {
    "id": 1,
    "event_id": 1,
    "performer_id": 2,
    "status": "pending",
    "applied_at": "2026-01-15T12:00:00"
  }
]
```

#### No Results Response

Status: `404`

```json
{
  "message": "No events found"
}
```

### GET `/applications/<application_id>`

Returns one application by ID.

#### Example

```http
GET /applications/1
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
{
  "id": 1,
  "event_id": 1,
  "performer_id": 2,
  "status": "pending",
  "applied_at": "2026-01-15T12:00:00"
}
```

#### Error Response

Status: `404`

```json
{
  "error": "Application not found"
}
```

### POST `/applications`

Creates a new application for a performer to apply to an event. New applications are created with a `pending` status.

#### Request Body

```json
{
  "event_id": 1,
  "performer_id": 2
}
```

#### Success Response

Status: `201`

```json
{
  "id": 1,
  "event_id": 1,
  "performer_id": 2,
  "status": "pending",
  "applied_at": "2026-01-15T12:00:00"
}
```

### PUT `/applications`

Updates an application status.

#### Request Body

```json
{
  "id": 1,
  "status": "approved"
}
```

#### Success Response

Status: `200`

```json
{
  "id": 1,
  "event_id": 1,
  "performer_id": 2,
  "status": "approved",
  "applied_at": "2026-01-15T12:00:00"
}
```

#### Error Response

Status: `404`

```json
{
  "error": "Application not found or update failed"
}
```

## Venues

### GET `/venues`

Returns all venues.

#### Example

```http
GET /venues
Authorization: Bearer <token>
```

#### Success Response

Status: `200`

```json
[
  {
    "id": 1,
    "name": "Main Stage"
  }
]
```

## Common Error Responses

### Missing Token

Status: `401`

```json
{
  "message": "Token is missing!"
}
```

### Expired Token

Status: `401`

```json
{
  "message": "Token has expired!"
}
```

### Invalid Token

Status: `401`

```json
{
  "message": "Token is invalid!"
}
```
