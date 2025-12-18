# meeting-scheduler-api
A Django REST API for scheduling meetings across timezones
# Meeting Scheduler API

A Django REST API for scheduling meetings across different timezones, considering participants' availability and working hours.

## Features
- User authentication and timezone management
- Event creation and management (busy/free times)
- Smart scheduling algorithm to find optimal meeting times
- Timezone-aware meeting scheduling
- RESTful API endpoints

## Tech Stack
- Django 4.2
- Django REST Framework
- SQLite (development) / PostgreSQL (production)
- pytz for timezone handling

## Installation
1. Clone repository
2. Create virtual environment
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Start server: `python manage.py runserver`
