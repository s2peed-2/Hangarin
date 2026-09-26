# Hangarin — Task & To-Do Manager

A small Django app for organizing daily tasks: priorities, categories,
subtasks, and notes, all manageable from the Django admin.

## Project layout

```
hangarin/
├── hangarin/            # project settings, urls, wsgi/asgi
├── todo/                # the app: models, admin, management command
│   ├── models.py        # BaseModel, Priority, Category, Task, SubTask, Note
│   ├── admin.py          # TaskAdmin, SubTaskAdmin, CategoryAdmin, PriorityAdmin, NoteAdmin
│   └── management/commands/populate_data.py   # seeds sample data with Faker
├── manage.py
├── requirements.txt
└── .gitignore
```

## 1. Set up the virtual environment

```bash
cd hangarin
python -m venv venv

# activate it
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

pip install -r requirements.txt
```

## 2. Create the database

```bash
python manage.py makemigrations todo
python manage.py migrate
python manage.py createsuperuser
```

## 3. Populate sample data

Priority and Category are seeded manually inside the command
(high/medium/low/critical/optional and Work/School/Personal/Finance/Projects),
while Task, SubTask, and Note are generated with Faker:

```bash
python manage.py populate_data
```

Pass `--tasks 50` if you want more than the default 30 tasks.

## 4. Run it locally

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/admin/` and log in with the superuser you
created. You'll see:

- **Tasks** — title, status, deadline, priority, category, with filters
  for status/priority/category and search on title/description.
- **Sub Tasks** — title, status, and the parent task's name, filterable
  by status and searchable by title.
- **Categories** / **Priorities** — just the name field, searchable,
  and displayed as "Categories" / "Priorities" in the sidebar instead
  of the grammatically-off "Categorys" / "Prioritys".
- **Notes** — task, content, created date, filterable by created date
  and searchable by content.

## 5. Version control

```bash
git init
git add .
git commit -m "Initial commit: Hangarin task manager"
```

`.gitignore` already excludes `venv/`, `db.sqlite3`, and other files
that shouldn't be tracked. To push to a remote:

```bash
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

## 6. Deploy to PythonAnywhere

1. **Push your code somewhere PythonAnywhere can reach**, e.g. GitHub,
   then on PythonAnywhere open a Bash console and clone it:
   ```bash
   git clone <your-repo-url>
   ```

2. **Create a virtualenv on PythonAnywhere** (still in the Bash console):
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 hangarin-env
   pip install -r hangarin/requirements.txt
   ```

3. **Create a new Web App** from the PythonAnywhere Web tab: choose
   "Manual configuration" and the matching Python version.

4. **Point it at your virtualenv**: on the Web tab, set the
   "Virtualenv" field to the path of `hangarin-env`
   (e.g. `/home/yourusername/.virtualenvs/hangarin-env`).

5. **Edit the WSGI file** (linked from the Web tab) so it points to
   your project. Replace its contents with something like:
   ```python
   import os
   import sys

   path = '/home/yourusername/hangarin'
   if path not in sys.path:
       sys.path.append(path)

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hangarin.settings')

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   ```

6. **Update settings for production**, in `hangarin/settings.py`:
   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']
   ```

7. **Run migrations and collect static files** in the Bash console
   (with the virtualenv active):
   ```bash
   cd hangarin
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py populate_data
   python manage.py collectstatic
   ```

8. **Map static files** on the Web tab: add a static file mapping with
   URL `/static/` pointing to `/home/yourusername/hangarin/staticfiles`.

9. Hit **Reload** on the Web tab and visit
   `https://yourusername.pythonanywhere.com/admin/`.

## Data model notes

- `BaseModel` is an abstract base class (`created_at`, `updated_at`)
  that `Priority`, `Category`, `Task`, `SubTask`, and `Note` all
  inherit from — that's where the timestamps come from on every table.
- `status` on `Task` and `SubTask` uses `choices`, so the admin form
  renders it as a dropdown instead of a free-text field.
- `Category` and `Priority` set `verbose_name_plural` in their `Meta`
  class so the admin sidebar reads "Categories" / "Priorities" rather
  than the default pluralization.
