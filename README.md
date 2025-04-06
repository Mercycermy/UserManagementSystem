```markdown
# Django Admin and User Management System

This is a Django-based web application that provides a simple but functional admin and user management system. The system includes user registration, login, password management, and admin tools to manage users via a dashboard.

This project was originally inspired by a PHP class project. I decided to build it using Django to enhance my understanding of Python web development and explore how Django handles authentication and user management out of the box.

## Features

### Admin Panel
- Admin login and logout
- View all registered users
- Add new users
- Edit user information
- Block or unblock users by toggling their staff status
- Delete users
- Search users by username

### User Side
- User registration
- User login and logout
- Change password

## Technologies Used

- Django (Python Framework)
- HTML Templates
- Django Authentication System

## Folder Structure

```
project/
├── templates/             # HTML files (adminhome, login, register, etc.)
├── views.py               # Admin and user logic
├── urls.py                # URL routes
├── models.py              # User model (using Django's default User model)
├── manage.py              # Django project manager
├── requirements.txt       # Python dependencies
```

## How to Run the Project

### Step 1: Clone the Repository

```bash
git clone https://github.com/mercycermy/usermanegment.git
cd django-user-admin
```

### Step 2: Set Up a Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r req.txt
```

### Step 4: Apply Migrations

```bash
python manage.py migrate
```

### Step 5: Create a Superuser

```bash
python manage.py createsuperuser
```

### Step 6: Run the Server

```bash
python manage.py runserver
```

## Access the Application

- Admin Panel: http://localhost:8000/adminlogin  
- User Login/Register: http://localhost:8000/login

## Notes

- Only superusers (`is_superuser=True`) can access the admin panel.
- The block/unblock feature toggles the `is_staff` flag to manage user access.
- Passwords are handled securely using Django's built-in authentication system.
- Custom views are used to separate admin and user functionality cleanly.

## Contribution

Contributions are welcome. If you notice a bug or have a suggestion for improvement:

1. Fork the repository
2. Make your changes
3. Submit a pull request

Alternatively, you can open an issue to discuss the changes.

