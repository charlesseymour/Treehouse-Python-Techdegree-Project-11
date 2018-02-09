# Treehouse-Python-Techdegree-Project-11: "Pug or Ugh"

# Description

Students had to write API views in Django to work with a supplied React front end script.
The app allows users to create an account and then browse profiles of dogs up for adoption,
marking them as liked, disliked, or undecided.</p>  

# Python

Version 3.6.0 

# Installing

- Download files.
- In the project directory install virtual environment: `python -m venv env`
- Activate virtual environment: in Windows `env\scripts\activate` or Posix `source env/bin/activate`
- Install requirements: `pip install -r requirements.txt`

# Database setup

- Go to 'backend' folder and run `python manage.py makemigrations`
- Then run `python manage.py migrate`
- Go to 'pugorugh/scripts' and run `python data_import.py` to populate the dog table.

# User setup

- Go back to 'backend' folder and run `python manage.py createsuperuser`
- Enter desired username, email, and password
- Then enter the shell: `python manage.py shell`
- Get token for superuser: 
   ```>>>from rest_framework.authtoken.models import Token`
   >>> from django.contrib.auth.models import User`
   >>> user = User.objects.get(id=1)`
   >>> token = Token.objects.create(user=user)`
   >>> token.key```
- Save the username, password, and token information.

# Running

- Start server: `python manage.py runserver 0.0.0.0:8000`
- Login using superuser name and password
- Set user preferences
- Mark some dogs as liked, disliked, and undecided.
- Test API requests using Postman.
