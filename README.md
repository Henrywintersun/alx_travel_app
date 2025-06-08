# alx_travel_app

ALX Travel App
A comprehensive Django REST API for travel listings, bookings, and reviews. This application provides a robust backend for managing travel accommodations, experiences, and user interactions.

Features
Travel Listings Management: Create, read, update, and delete travel listings (hotels, apartments, houses, experiences, restaurants)
User Reviews System: Rate and review listings with validation
Booking Management: Handle reservations with status tracking
RESTful API: Full REST API with proper HTTP methods and status codes
API Documentation: Automatic Swagger/OpenAPI documentation
Database: MySQL integration with proper relationships
Authentication: Django's built-in authentication system
CORS Support: Cross-origin resource sharing for frontend integration
Celery Integration: Asynchronous task processing
Admin Interface: Django admin for easy data management
Technology Stack
Framework: Django 4.2.7
API: Django REST Framework 3.14.0
Database: MySQL with mysqlclient 2.2.0
Documentation: drf-yasg 1.21.7 (Swagger/OpenAPI)
Task Queue: Celery 5.3.4 with Redis
CORS: django-cors-headers 4.3.1
Environment: django-environ 0.11.2
Project Structure
alx_travel_app/
├── alx_travel_app/
│   ├── __init__.py
│   ├── settings.py          # Main settings with environment variables
│   ├── urls.py              # URL routing with Swagger integration
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py            # Celery configuration
├── listings/
│   ├── __init__.py
│   ├── models.py            # Database models (Listing, Review, Booking)
│   ├── views.py             # API viewsets
│   ├── serializers.py       # Data serialization
│   ├── urls.py              # App-specific URLs
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   └── signals.py           # Django signals for automated tasks
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules
├── manage.py               # Django management script
└── README.md               # This file
Setup Instructions
1. Clone the Repository
bash
git clone https://github.com/yourusername/alx_travel_app.git
cd alx_travel_app
2. Create Virtual Environment
bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Database Setup
Install MySQL (if not already installed)
Create Database:
sql
CREATE DATABASE alx_travel_db;
CREATE USER 'your_db_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON alx_travel_db.* TO 'your_db_user'@'localhost';
FLUSH PRIVILEGES;
5. Environment Configuration
Copy environment template:
bash
cp .env.example .env
Update .env file with your configuration:
env
DB_NAME=alx_travel_db
DB_USER=your_db_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
6. Database Migration
bash
python manage.py makemigrations
python manage.py migrate
7. Create Superuser
bash
python manage.py createsuperuser
8. Run Development Server
bash
python manage.py runserver
The application will be available at http://localhost:8000/

API Endpoints
Swagger Documentation
Swagger UI: http://localhost:8000/swagger/
ReDoc: http://localhost:8000/redoc/
Core Endpoints
Listings
GET /api/v1/listings/ - List all listings
POST /api/v1/listings/ - Create new listing
GET /api/v1/listings/{id}/ - Get specific listing
PUT /api/v1/listings/{id}/ - Update listing
DELETE /api/v1/listings/{id}/ - Delete listing
GET /api/v1/listings/my_listings/ - Get current user's listings
GET /api/v1/listings/{id}/reviews/ - Get reviews for a listing
Reviews
GET /api/v1/reviews/ - List all reviews
POST /api/v1/reviews/ - Create new review
GET /api/v1/reviews/{id}/ - Get specific review
PUT /api/v1/reviews/{id}/ - Update review
DELETE /api/v1/reviews/{id}/ - Delete review
GET /api/v1/reviews/my_reviews/ - Get current user's reviews
Bookings
GET /api/v1/bookings/ - List user's bookings
POST /api/v1/bookings/ - Create new booking
GET /api/v1/bookings/{id}/ - Get specific booking
PUT /api/v1/bookings/{id}/ - Update booking
DELETE /api/v1/bookings/{id}/ - Delete booking
POST /api/v1/bookings/{id}/cancel/ - Cancel booking
POST /api/v1/bookings/{id}/confirm/ - Confirm booking
Features
Filtering and Search
Listings: Filter by type, availability, location; search by title, description, location
Reviews: Filter by rating, listing
Bookings: Filter by status, listing
Authentication
Token-based authentication
Session authentication for browsable API
Permission-based access control
Validation
Comprehensive data validation
Custom business logic validation
Proper error handling with meaningful messages
Celery Tasks
Set up for asynchronous task processing (email notifications, data processing, etc.)

bash
# Start Celery worker (in separate terminal)
celery -A alx_travel_app worker --loglevel=info

# Start Celery beat scheduler (for periodic tasks)
celery -A alx_travel_app beat --loglevel=info
Admin Interface
Access the Django admin at http://localhost:8000/admin/ using your superuser credentials.

Features:

Comprehensive listing management
Review moderation
Booking oversight
User management
Development
Running Tests
bash
python manage.py test
Database Reset
bash
python manage.py flush
python manage.py migrate
Static Files
bash
python manage.py collectstatic
Production Deployment
Set DEBUG=False in environment
Configure proper ALLOWED_HOSTS
Use environment variables for all sensitive data
Set up proper logging
Configure web server (nginx/Apache)
Use production database settings
Set up Redis for Celery in production
Contributing
Fork the repository
Create a feature branch
Make your changes
Add tests if applicable
Submit a pull request
License
This project is licensed under the MIT License.

Support
For support, please contact the development team or create an issue in the repository.

