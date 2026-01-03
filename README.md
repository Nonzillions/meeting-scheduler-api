📅 Meeting Scheduler API
A Django REST Framework API that intelligently schedules meetings across multiple users by analyzing availability across different timezones and working hours.

✨ Core Features
🔐 Smart Authentication: Register, log in, and manage user sessions with timezone preferences.

📅 Intelligent Scheduling: The core algorithm finds all available time slots where specified users are free, respecting their working hours and existing events.

⏰ Timezone-Aware: All scheduling is handled in UTC, with automatic conversion based on user profiles.

🚀 RESTful API: Clean, predictable endpoints for easy integration with frontend applications.

⚙️ Full CRUD Operations: Create, read, update, and delete events to manage user calendars.

🛠 Tech Stack
Backend Framework: Django 4.2 & Django REST Framework

Database: SQLite (Development) / PostgreSQL (Production on Heroku)

Authentication: Django Session Authentication & Django REST Framework

Timezone Handling: pytz library

Production Server: Gunicorn

Static Files: Whitenoise

Deployment: Heroku

📋 Prerequisites
Before you begin, ensure you have the following installed:

Python 3.8 or higher

pip (Python package manager)

Git

(Optional) A virtual environment tool (venv or virtualenv)

Detailed Authentication & User Management
This API provides a complete session-based authentication system.

Base URL for Authentication
All authentication endpoints are prefixed with: http://localhost:8000/api/auth/

Available Endpoints
1. User Registration
Creates a new user account and automatically logs them in.

Endpoint: POST /api/auth/register/

Description: Accepts user details, creates an account, hashes the password, and establishes a login session.

Request Body (JSON):

json
{
  "username": "alice_dev",
  "password": "securePass123",
  "email": "alice@example.com",
  "timezone": "America/Los_Angeles"
}
cURL Example:

bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_dev",
    "password": "securePass123",
    "email": "alice@example.com",
    "timezone": "America/Los_Angeles"
  }'
Success Response (201 Created):

json
{
  "message": "User registered successfully",
  "user": {
    "id": 4,
    "username": "alice_dev",
    "email": "alice@example.com",
    "timezone": "America/Los_Angeles",
    "working_hours_start": "09:00:00",
    "working_hours_end": "17:00:00"
  }
}
2. User Login
Authenticates an existing user and creates a session.

Endpoint: POST /api/auth/login/

Description: Validates credentials and logs the user in.

Request Body (JSON):

json
{
  "username": "alice_dev",
  "password": "securePass123"
}
cURL Example:

bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_dev",
    "password": "securePass123"
  }'
Success Response (200 OK):

json
{
  "message": "Login successful",
  "user": {
    "id": 4,
    "username": "alice_dev",
    "email": "alice@example.com",
    "timezone": "America/Los_Angeles"
  }
}
3. User Logout
Terminates the current user's session.

Endpoint: POST /api/auth/logout/

Description: Logs out the currently authenticated user. Requires an active session.

cURL Example:

bash
curl -X POST http://localhost:8000/api/auth/logout/ \
  -b "sessionid=<your_session_cookie>"
(Note: You typically need to include the session cookie from a successful login.)

Success Response (200 OK):

json
{
  "message": "Logout successful"
}
4. View User Profile
Retrieves details of the currently logged-in user.

Endpoint: GET /api/auth/profile/

Description: A protected endpoint that returns information about the authenticated user.

cURL Example:

bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -b "sessionid=<your_session_cookie>"
Success Response (200 OK):

json
{
  "id": 4,
  "username": "alice_dev",
  "email": "alice@example.com",
  "timezone": "America/Los_Angeles",
  "working_hours_start": "09:00:00",
  "working_hours_end": "17:00:00"
}
5. Update User Profile
Allows the user to update their profile information.

Endpoint: PUT /api/auth/profile/

Description: Updates fields for the logged-in user. Uses partial=True so you can update individual fields.

Request Body (JSON - Example updating timezone):

json
{
  "timezone": "Europe/London"
}
cURL Example:

bash
curl -X PUT http://localhost:8000/api/auth/profile/ \
  -H "Content-Type: application/json" \
  -b "sessionid=<your_session_cookie>" \
  -d '{"timezone": "Europe/London"}'
Success Response (200 OK):

json
{
  "id": 4,
  "username": "alice_dev",
  "email": "alice@example.com",
  "timezone": "Europe/London",
  "working_hours_start": "09:00:00",
  "working_hours_end": "17:00:00"
}
📅 Event Management API
Manage calendar events (mark times as busy or free).

Base URL: http://localhost:8000/api/events/

Key Endpoints:
GET /api/events/ - List all events for the authenticated user.

POST /api/events/ - Create a new event.

json
// Request Body
{
  "title": "Project Kickoff",
  "start_time": "2025-12-30T14:00:00Z",
  "end_time": "2025-12-30T15:30:00Z",
  "event_type": "busy",
  "description": "Meeting with the client"
}
GET /api/events/{id}/ - Retrieve a specific event.

PUT /api/events/{id}/ - Update an event.

DELETE /api/events/{id}/ - Delete an event.

⚡ Core Scheduling API
The heart of the application. Finds common free slots between users.

Endpoint: POST /api/scheduling/find-slots/

Description: Takes a list of user IDs and a meeting duration, then calculates all overlapping free slots within a default 7-day window, respecting working hours (9 AM-5 PM).

Request Body (JSON):

json
{
  "user_ids": [1, 4, 7],
  "duration_minutes": 60
}
cURL Example:

bash
curl -X POST http://localhost:8000/api/scheduling/find-slots/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [1, 4],
    "duration_minutes": 60
  }'
Success Response (200 OK) - Example:

json
{
  "available_slots": [
    {
      "start_time": "2025-12-29T09:00:00+00:00",
      "end_time": "2025-12-29T10:00:00+00:00"
    },
    {
      "start_time": "2025-12-29T09:30:00+00:00",
      "end_time": "2025-12-29T10:30:00+00:00"
    }
  ],
  "user_ids": [1, 4],
  "duration_minutes": 60,
  "total_slots_found": 119
}
*This result shows 119 possible 1-hour meetings over 7 days for the given users.*

