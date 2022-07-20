# Car Selling

## Features:
- Make on Windows 11
- Uses Django 
- Django Provides Us An Admin Page To Manipulate Data
- Statically Generate User Friendly UI
- User Authentication 
- PostgreSQL Database (Faster And Developer Friendly)

> Car Selling Is A Website Powered By Django That Enables Server Side Rendering Most Commonly Known As (SSR)

## Tools And Technologies Used:
1. Django 
2. JavaScript 
3. HTML/CSS 
4. BootStrap 
5. GitHub
6. Python
7. Bash/CMD 

## Django 
1. Clone Repo to A Folder

> Creating a virtual environment is not necessary
2. Create A Virtual Env 
```sh
py venv (VENV Name) 
cd (VENV Name)
source bin /activate (BASH)
```
3. Install Django Using Pip 
```sh
pip install django django-ckeditor django-multiselectfield
```
4. Create Database in PostgreSQL, Makemigrations, Migrate the migrations to the DB, Create a uper user and collect static files e.g., css, js and fonts
```sh
py manage.py makemigrations
py manage.py migrate
py manage.py createsuperuser
py manage.py collectstatic
```
5. Run Python Server 
```sh
python manage.py runserver
```
