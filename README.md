# task_manager_backend
This project is a Django-based API with token authentication using Django REST framework and JWT. Below are the instructions to set up and run the project.

1. Clone the Repository
Open your terminal and run:
bash
git clone https://github.com/DILEESHA09/task_manager_backend.git
cd task_manager_django
2. Set Up a Virtual Environment
Create and activate a virtual environment:
bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows
.\env\Scripts\activate
# On macOS/Linux
source env/bin/activate
3. Install Dependencies
Install the required packages:
bash
pip install -r requirements.txt
Update your database settings in settings.py:
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<database_name>',
        'USER': '<your_postgres_username>',
        'PASSWORD': '<your_postgres_password>',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
5. Run Migrations
Apply the database migrations:
bash
python manage.py migrate
6. Run the Development Server
Start the Django server:
python manage.py runserver
Open your browser and go to http://127.0.0.1:8000/ to access the API.
