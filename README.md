# Django Development Guide

This guide provides detailed instructions for setting up and starting a Django application using Python virtual environments.

## What is a Virtual Environment?

A virtual environment is an isolated Python environment that allows you to install packages and dependencies specific to your project without affecting your system-wide Python installation. This prevents version conflicts and keeps your projects organized.

## Prerequisites

- Python 3.7 or higher installed on your system
- Basic knowledge of command line/terminal usage

## Step-by-Step Setup Instructions

### 1. Create a Virtual Environment

Navigate to your project directory and create a virtual environment:

```bash
# Create a virtual environment named 'env' (you can use any name)
python -m venv env

# On some systems, you might need to use python3
python3 -m venv env
```

### 2. Activate the Virtual Environment

**On macOS/Linux:**

```bash
source env/bin/activate
```

**On Windows:**

```bash
# Command Prompt
env\Scripts\activate

# PowerShell
env\Scripts\Activate.ps1
```

When activated, you should see `(env)` at the beginning of your command prompt, indicating the virtual environment is active.

### 3. Install Django

With the virtual environment activated, install Django:

```bash
pip install django

# To install a specific version (recommended for production)
pip install django==4.2.25
```

### 4. Create a Django Project

Create a new Django project:

```bash
# Replace 'myproject' with your desired project name
django-admin startproject myproject
cd myproject
```

### 5. Run the Development Server

Start the Django development server:

```bash
python manage.py runserver
```

Your Django application will be available at `http://127.0.0.1:8000/` or `http://localhost:8000/`

### 6. Create Your First App (Optional)

To create a Django app within your project:

```bash
python manage.py startapp myapp
```

Don't forget to add your app to `INSTALLED_APPS` in `settings.py`.

## Development Workflow

### Daily Development

1. **Activate your virtual environment** before working:

   ```bash
   source env/bin/activate  # macOS/Linux
   env\Scripts\activate     # Windows
   ```

2. **Install new packages** (when needed):

   ```bash
   pip install package_name
   ```

3. **Run migrations** (when you make model changes):

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Start the development server**:

   ```bash
   python manage.py runserver
   ```

5. **Deactivate** when done:
   ```bash
   deactivate
   ```

### Managing Dependencies

Create a requirements file to track your project dependencies:

```bash
# Generate requirements.txt
pip freeze > requirements.txt

# Install from requirements.txt (useful for team collaboration)
pip install -r requirements.txt
```

## Common Commands Cheat Sheet

| Command                               | Description                                |
| ------------------------------------- | ------------------------------------------ |
| `python -m venv env`                  | Create virtual environment                 |
| `source env/bin/activate`             | Activate virtual environment (macOS/Linux) |
| `env\Scripts\activate`                | Activate virtual environment (Windows)     |
| `deactivate`                          | Deactivate virtual environment             |
| `pip install django`                  | Install Django                             |
| `django-admin startproject myproject` | Create new Django project                  |
| `python manage.py startapp myapp`     | Create new Django app                      |
| `python manage.py runserver`          | Start development server                   |
| `python manage.py makemigrations`     | Create database migrations                 |
| `python manage.py migrate`            | Apply database migrations                  |
| `python manage.py createsuperuser`    | Create admin user                          |
| `pip freeze > requirements.txt`       | Export dependencies                        |

## Troubleshooting

### Virtual Environment Not Activating

- Make sure you're in the correct directory
- Check that the virtual environment was created successfully
- On Windows, you might need to enable script execution: `Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser`

### Django Command Not Found

- Ensure your virtual environment is activated
- Verify Django is installed: `pip list | grep Django`

### Port Already in Use

- Use a different port: `python manage.py runserver 8001`
- Or kill the process using the port

## Next Steps

After setting up your Django project:

1. Configure your database settings in `settings.py`
2. Create your models in `models.py`
3. Set up URL routing in `urls.py`
4. Create views in `views.py`
5. Design templates in the templates directory
6. Add static files (CSS, JavaScript, images)

Happy coding! 🚀
