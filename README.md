Django Admin and User Management System


This project is a simple Django web application for managing users through an admin panel. It supports admin login, user registration, user login, and profile management features like editing, blocking, deleting, and password changes.

-Features
    Admin Side
    Admin login/logout
    View all registered users
    Add new users
    Edit user details
    Block/unblock users (toggle staff status)
    Delete users
    Search users by username
-User Side
   Register a new user
   Login/logout
   Change password
-Technologies Used
   Django (Python Framework)
   HTML templates
   Django Authentication system

Folder Structure
views.py: Contains all admin and user views
templates/: HTML files for frontend (adminhome, login, register, changepassword, etc.)
urls.py: URL patterns for routing

How to Run the Project
1 Clone the Repository
      git clone https://github.com/mercycermy/usermanegment.git
      cd django-user-admin

2 Set up a virtual environment (optional but recommended)
      python -m venv venv
      source venv/bin/activate  # On Windows use venv\Scripts\activate

3 Install Dependencies
     pip install -r req.txt

4 Run Migrations
        python manage.py migrate

5  Create a Superuser
    python manage.py createsuperuser

6   Run the Server
      python manage.py runserver


                  Access the App
Admin Panel: http://localhost:8000/adminlogin

User Login/Register: http://localhost:8000/login

Notes
Only users with is_superuser=True can log in as admin.

Blocking a user will toggle their is_staff status.

You can manage passwords securely using Django's built-in tools.

Contribution
Feel free to fork and contribute. If you spot a bug or have a suggestion, submit an issue or a pull request.