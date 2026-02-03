# Setup Steps

## 1. Clone the repository

```
git clone <repository-url>
cd <project-directory>
```

## 2. Create and activate a virtual environment

```
python -m venv venv
```

### Windows

```
venv\Scripts\activate
```


## 3. Install dependencies

```
pip install -r requirements.txt
```

## 4. Configure the database (MySQL)

Create a MySQL database and user:

```
CREATE DATABASE clinic_db CHARACTER SET utf8mb4;

CREATE USER 'clinic_user'@'localhost'
IDENTIFIED WITH mysql_native_password BY 'password123';

GRANT ALL PRIVILEGES ON clinic_db.* TO 'clinic_user'@'localhost';
FLUSH PRIVILEGES;
```

Update settings.py:

```
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "clinic_db",
        "USER": "clinic_user",
        "PASSWORD": "password123",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

## 5. Run migrations

```
python manage.py makemigrations
python manage.py migrate
```

# Creating a Superuser

Create an admin user to access Django Admin:

```
python manage.py createsuperuser
```

Follow the prompts to set username and password.

# Creating Clinic and UserProfile

Start the server:

```
python manage.py runserver
```

Open Django Admin:

```
http://127.0.0.1:8000/admin/
```

## Create a Clinic

Admin → Clinics → Add

## Create a UserProfile

Admin → UserProfiles → Add

Select:

User → the created user

Clinic → the created clinic

Each user must have a UserProfile linked to a Clinic to access the dashboard.

# Running Tests

Run all automated tests using:

```
python manage.py test
```

This runs tests covering authentication, authorization, token generation, and public view logging.

# Running CSV Import

A management command is provided to import follow-ups from a CSV file.

## CSV format

```
patient_name,phone,due_date,language,notes
Rahul Sharma,9876543210,2026-02-10,en,First visit
Anita Verma,9123456780,2026-02-12,hi,Follow-up required
```

Run import command

```
python manage.py import_followups --csv sample.csv --username <username>
```

Valid rows are imported

Invalid rows are skipped

A summary is printed after execution

# Notes

Public user signup is intentionally disabled

Users are created via Django Admin

All data access is restricted to the user’s clinic
