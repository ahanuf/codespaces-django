🛠️ Django Web App – GitHub Codespaces Ready
Welcome to your fully containerized Django project running inside GitHub Codespaces! This project scaffold is perfect for rapid development, experimentation, and deployment of Django applications.

Whether you're building a blog, an API backend, or a full-stack platform, this README gives you everything you need to get started.

🚀 Getting Started
This project is pre-configured to work inside GitHub Codespaces with Python 3.12 and Django 5.1.7. It includes essential packages, tools, and tips to guide development.

📦 Installing Dependencies
Install all required packages using pip:

bash
Copy
Edit
pip install -r requirements.txt
Make sure you're in the virtual environment. If not, activate it with:

bash
Copy
Edit
source .venv/bin/activate
🗃️ Project Structure
Here's a quick look at the project layout:

php
Copy
Edit
.
├── apps/                 # Your Django apps live here
│   └── models.py         # Custom models (e.g., Post model with slug support)
├── manage.py             # Django's CLI utility
├── requirements.txt      # Project dependencies
├── templates/            # HTML templates
├── static/               # Static assets (CSS, JS, images)
├── .devcontainer/        # Codespaces configuration
└── README.md             # You're reading it!
🔧 Running the Server
Launch the Django development server:

bash
Copy
Edit
python manage.py runserver
Once running, visit:

http://localhost:8000 → your Django site

http://localhost:8000/admin → Django admin panel

🧊 Collecting Static Files
To collect all static assets into the STATIC_ROOT directory (e.g., for deployment):

bash
Copy
Edit
python manage.py collectstatic
🔐 Authentication (Django Allauth)
This project uses django-allauth for login, signup, and account management. URLs include:

/accounts/login/

/accounts/signup/

/accounts/logout/

Ensure you have the following in your INSTALLED_APPS:

python
Copy
Edit
INSTALLED_APPS = [
    ...
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
]
And:

python
Copy
Edit
SITE_ID = 1
LOGIN_REDIRECT_URL = '/'
🧪 Recommended Development Tools
GitHub Codespaces (VS Code Dev Containers)

SQLite3 for local DB (easy setup)

Django Debug Toolbar (for profiling)

dotenv for managing local secrets

📌 Common Issues & Fixes
❌ CSRF Verification Failed:
Add this to settings.py for local dev:

python
Copy
Edit
CSRF_TRUSTED_ORIGINS = ["http://localhost:8000"]
❌ IntegrityError on slug:
Your Post model includes unique slugs. If you see this:

sql
Copy
Edit
UNIQUE constraint failed: apps_post.slug
Make sure slug generation logic in models.py ensures uniqueness (auto-appends -1, -2, etc.)

🌐 Deployment Notes
When you're ready to deploy:

Set DEBUG = False

Set ALLOWED_HOSTS = ['yourdomain.com']

Configure DATABASES for PostgreSQL or production DB

Use WhiteNoise or other middleware to serve static files

Use gunicorn or daphne for production web server

📤 Publishing to GitHub
If this codespace isn't connected to a repo yet:

Click "Publish Branch" in the GitHub Codespaces toolbar.

GitHub will create a repository and push this project.

Collaborators can now clone, fork, or open in their own codespaces.

🙏 Credits
This project bootstrapped with:

Django (https://www.djangoproject.com/)

GitHub Codespaces

django-allauth

SQLite for dev DB

📃 License
This project is licensed under the MIT License. Feel free to use, modify, and distribute it for personal or commercial use.