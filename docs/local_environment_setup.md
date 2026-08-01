# Local Environment Setup

This guide walks through setting up the Performer Booking API on your local machine with Python and a local PostgreSQL database running in Docker.

## Prerequisites

Install the following before getting started:

- Git
- Python 3.11
- Docker Desktop
- PostgreSQL command line tools, including `psql`
- Postman, or another API testing tool

## 1. Clone the Repository

```bash
git clone https://github.com/darasjohn15/booking-app-apis.git
cd booking-app-apis
```

## 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows, activate the virtual environment with:

```bash
venv\Scripts\activate
```

## 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 4. Start PostgreSQL with Docker

The repo includes a `docker-compose.yml` file with a PostgreSQL service configured for local development.

```bash
docker compose up -d db
```

This starts a PostgreSQL container with:

| Setting  | Value          |
| -------- | -------------- |
| Host     | `localhost`    |
| Port     | `5433`         |
| Database | `appdb`        |
| User     | `app_user`     |
| Password | `app_password` |

## 5. Create a Local `.env` File

Create a `.env` file in the project root:

```bash
touch .env
```

Add the following environment variables:

```env
DB_HOST=localhost
DB_NAME=appdb
DB_USER=app_user
DB_PASSWORD=app_password
DB_PORT=5433
DB_SSLMODE=disable
CORS_ORIGINS=http://localhost:4200
```

The Flask app and database setup scripts read these values when connecting to PostgreSQL.

## 6. Create the Database Tables

Run the table deployment script:

```bash
python deploy_tables.py
```

This creates the local database tables for:

- `users`
- `events`
- `applications`
- `venues`

## 7. Deploy the SQL Functions

The API uses PostgreSQL functions from the `sql/` folder for data access. Deploy them after creating the tables:

```bash
python deploy_sql.py
```

If this command fails because `psql` is not installed, install the PostgreSQL command line tools and run the command again.

## 8. Add a Test Venue

The API can retrieve venues, but it does not currently expose an endpoint to create venues. Add at least one venue directly in PostgreSQL so events can be associated with a venue:

```bash
psql -h localhost -p 5433 -U app_user -d appdb
```

When prompted, enter:

```text
app_password
```

Then run:

```sql
INSERT INTO venues (name)
VALUES ('Main Stage')
ON CONFLICT DO NOTHING;
```

Exit `psql`:

```sql
\q
```

## 9. Run the API

Start the Flask API:

```bash
python Main.py
```

The API runs at:

```text
http://127.0.0.1:8085
```

## 10. Verify the API

Open a browser or Postman and call the health check endpoint:

```http
GET http://127.0.0.1:8085/ping
```

Expected response:

```json
{
  "status": "Ok"
}
```

## 11. Create a User

Create a user before trying protected endpoints.

```http
POST http://127.0.0.1:8085/users
Content-Type: application/json
```

Example request body:

```json
{
  "name": "Host User",
  "email": "host@example.com",
  "password": "password123",
  "role": "host"
}
```

## 12. Log In and Use the JWT Token

Log in with the user credentials:

```http
POST http://127.0.0.1:8085/login
Content-Type: application/json
```

Example request body:

```json
{
  "email": "host@example.com",
  "password": "password123"
}
```

Copy the returned `token` value and include it in protected requests:

```http
Authorization: Bearer <token>
```

## 13. Run Tests

Run the test suite with:

```bash
pytest
```

## Common Commands

Stop the local PostgreSQL container:

```bash
docker compose down
```

Stop the container and remove the local database volume:

```bash
docker compose down -v
```

Restart the database:

```bash
docker compose up -d db
```

## Troubleshooting

### Missing Database Environment Variables

If you see this error:

```text
Missing one or more required DB environment variables
```

Confirm that the `.env` file exists in the project root and includes `DB_HOST`, `DB_NAME`, `DB_USER`, and `DB_PASSWORD`.

### Database Connection Failed

Confirm the Docker database is running:

```bash
docker compose ps
```

For local Python development, `DB_HOST` should be `localhost` and `DB_PORT` should be `5433`.

### Protected Endpoint Returns 401

Make sure you are sending the JWT token from `POST /login` in the request headers:

```http
Authorization: Bearer <token>
```

### Creating an Event Fails

Events require a `venueID` in the request body. Since venues are not created through the API, confirm that at least one venue exists in the `venues` table.
