# Hangarin — Task & To-Do Manager

A Django web app for organizing daily tasks: priorities, categories,
subtasks, and notes. Users can sign in with a username/password, Google,
or GitHub.

- Live site: https://cyrek2.pythonanywhere.com
- Source code: https://github.com/s2peed-2/Hangarin

## Features

- Models: `Priority`, `Category`, `Task`, `SubTask`, `Note` (all inherit
  `created_at` / `updated_at` from an abstract `BaseModel`)
- Django admin with list display, filters, and search for each model
- Sample data generated with Faker
- Login with Google and GitHub using django-allauth

## Run it locally

```bash
python -m venv venv
venv\Scripts\activate            # Windows
source venv/bin/activate         # macOS / Linux

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py populate_data   # optional: adds sample data
python manage.py runserver
```

Open http://127.0.0.1:8000/ for the app or http://127.0.0.1:8000/admin/ for the admin.

## Social login

The Google and GitHub client IDs and secrets are not stored in the code.
They are added in the Django admin under **Social applications**, so they
are never committed to Git.

## Deployment

Deployed on PythonAnywhere. `settings.py` detects the server automatically
and switches `DEBUG`, `SITE_ID`, and `ALLOWED_HOSTS`.