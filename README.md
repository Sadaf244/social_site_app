# Social-Site Application

This is a social networking application built with Django and Django Rest Framework. The project is containerized using Docker.

## Setup Instructions
### Step 1: Clone the Repository
git clone https://github.com/Sadaf244/social_site_app.git
cd social_site_app

##Step 2: Create and Activate Virtual Environment
If you prefer to run the project without Docker, you can create a virtual environment:
python -m venv env
Activate the virtual environment:
env\Scripts\activate

##Step 3: Install Dependencies
Install the required Python packages:
pip install -r requirements.txt

##Step 4: Dockerization
Build and run the Docker containers:
docker-compose build
docker-compose up

##Step 5: Database Migrations
Run the database migrations:
docker-compose exec web python manage.py migrate

##Step 6: Create Superuser
Create a superuser to access the Django admin:
docker-compose exec web python manage.py createsuperuser
Access the Application
The application will be available at http://localhost:8000
