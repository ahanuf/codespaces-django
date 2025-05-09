# GitHub Codespaces ❤️ Django

Welcome to your Django project set up with GitHub Codespaces! This README will guide you through configuration, development, testing, and deployment best practices to get the most out of your new Django application.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#getting-started)

   * [Cloning the Repo](#cloning-the-repo)
   * [Setting Up the Codespace](#setting-up-the-codespace)
   * [Installing Dependencies](#installing-dependencies)
   * [Environment Configuration](#environment-configuration)
4. [Running the Application](#running-the-application)

   * [Development Server](#development-server)
   * [Collecting Static Files](#collecting-static-files)
5. [Database Migrations & Models](#database-migrations--models)
6. [Slug Generation & Uniqueness](#slug-generation--uniqueness)
7. [Testing](#testing)

   * [Unit Tests](#unit-tests)
   * [Coverage](#coverage)
8. [Linting & Formatting](#linting--formatting)
9. [Debugging & Logging](#debugging--logging)
10. [Docker & Containerization](#docker--containerization)
11. [CI/CD Integration](#ci-cd-integration)
12. [Deployment](#deployment)
13. [Environment Variables](#environment-variables)
14. [Troubleshooting](#troubleshooting)
15. [Contributing](#contributing)
16. [License](#license)
17. [Acknowledgments](#acknowledgments)

---

## Project Overview

This repository contains a Django-based web application scaffolded inside GitHub Codespaces. It includes support for:

* Rapid development with live code reloading
* Secure settings management via environment variables
* Automated slug generation with unique constraints
* Database migrations, testing, and code quality checks
* Optional Docker and CI/CD pipelines for production deployment

## Prerequisites

Before you begin, ensure you have the following installed:

* **GitHub Account**: for Codespaces and repository hosting.
* **GitHub Codespaces**: enabled on your account or organization.
* **Python** 3.11+ (managed by Codespaces; local version optional).
* **pip** (comes with Python).
* **PostgreSQL** (recommended) or **SQLite** for development.
* **Docker** (if using containerization).

## Getting Started

### Cloning the Repo

> *Note: If you haven't published your codespace branch yet, click **Publish Branch** in the Codespaces UI to create the GitHub repo.*

```bash
# After publishing, clone your repository locally:
git clone git@github.com:<your-username>/<your-repo>.git
cd <your-repo>
```

### Setting Up the Codespace

1. Click **Code** → **Open with Codespaces**.
2. Choose an existing codespace or create a new one.
3. The dev container will build automatically, installing Python and dependencies.

### Installing Dependencies

Install Python dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Environment Configuration

Create a `.env` file in the project root (this is ignored by Git by default):

```
DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgres://user:password@localhost:5432/dbname
ALLOWED_HOSTS=localhost,127.0.0.1
```

Load environment variables automatically with `python-dotenv` or `django-environ` in `settings.py`.

## Running the Application

### Development Server

Start the Django development server:

```bash
python manage.py runserver 0.0.0.0:8000
```

Visit [http://localhost:8000](http://localhost:8000) in your browser.

### Collecting Static Files

Before deploying, collect static assets:

```bash
python manage.py collectstatic --noinput
```

## Database Migrations & Models

* Create new migrations after changing models:

  ```bash
  python manage.py makemigrations
  python manage.py migrate
  ```

* If using PostgreSQL, ensure the `psycopg2` or `psycopg[binary]` driver is installed.

## Slug Generation & Uniqueness

The `Post` model includes a `slug` field with unique constraints. Slugs are auto-generated in `models.py`:

```python
from django.db import models
from django.utils.text import slugify
import itertools

class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    # other fields...

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)[:50]
            slug_candidate = base_slug
            for i in itertools.count(1):
                if not Post.objects.filter(slug=slug_candidate).exists():
                    break
                slug_candidate = f"{base_slug}-{i}"[:60]
            self.slug = slug_candidate
        super().save(*args, **kwargs)
```

This ensures each slug is unique by appending numeric suffixes as needed.

## Testing

### Unit Tests

Run all tests with:

```bash
python manage.py test
```

### Coverage

Generate a coverage report (requires `coverage` package):

```bash
coverage run --source='.' manage.py test
coverage report
coverage html
```

Open `htmlcov/index.html` to view detailed coverage.

## Linting & Formatting

* **flake8** for linting:

  ```bash
  flake8 .
  ```

* **black** for code formatting:

  ```bash
  black .
  ```

* **isort** for import sorting:

  ```bash
  isort .
  ```

## Debugging & Logging

* Use Django’s built-in logging configuration in `settings.py`.
* Install `django-debug-toolbar` for interactive debugging panels.

## Docker & Containerization

A sample `Dockerfile` and `docker-compose.yml` are provided:

```dockerfile
# Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "apps.wsgi:application", "--bind", "0.0.0.0:8000"]
```

```yaml
# docker-compose.yml
version: '3.9'
services:
  web:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - ./.env
    depends_on:
      - db
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: django_db
      POSTGRES_USER: django_user
      POSTGRES_PASSWORD: password
```

Bring up the stack:

```bash
docker-compose up --build
```

## CI/CD Integration

We recommend using GitHub Actions. A sample workflow `.github/workflows/ci.yml` includes:

* Dependency installation
* Linting
* Testing with coverage
* Docker image build

## Deployment

Guidelines for deployment platforms:

* **Heroku**: Use `Procfile`, set environment variables in dashboard.
* **AWS Elastic Beanstalk**: Configure `ebextensions` and use `gunicorn`.
* **Docker Swarm / Kubernetes**: Deploy service definitions with `kubectl`.

## Environment Variables

Store secrets and configuration in environment:

| Variable       | Purpose                      |
| -------------- | ---------------------------- |
| SECRET\_KEY    | Django secret key            |
| DEBUG          | `True` for dev, `False` prod |
| DATABASE\_URL  | DB connection URL            |
| ALLOWED\_HOSTS | Comma-separated hostnames    |

## Troubleshooting

* **IntegrityError: UNIQUE constraint failed**: Ensure slug uniqueness logic is in place. Delete conflicting slug or adjust title.
* **CSRF verification failed**: Add your domain to `CSRF_TRUSTED_ORIGINS` in `settings.py`.

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/xyz`)
3. Commit your changes (`git commit -m 'Add xyz'`)
4. Push to the branch (`git push origin feature/xyz`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

* Thanks to the Django community and GitHub Codespaces for streamlining development workflows.
* Inspired by various community boilerplates and best practices.
