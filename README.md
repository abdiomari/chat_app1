# chat_app1 — Real-time Chat Application Built with Django and Channels

## Overview
This project is a simple chat application that allows users to create a chat room and engage in real-time conversations with others. It is built using Django, a high-level Python web framework, and Channels, a library for building real-time web applications.

## Tech Stack
* Python 3.10
* Django 4.x
* Channels 3.x
* Django Channels Redis
* SQLite Database

## Features
* Real-time chat room creation and management
* User authentication and authorization
* Group chat functionality
* Message sending and receiving
* Room listing and joining

## Screenshots
> 📸 Screenshots coming soon. Run the project locally to see it in action.

## Setup & Installation
To get started with this project, follow these steps:

1. Clone the repository using the following command:
```bash
git clone https://github.com/abdiomari/chat_app1.git
```
2. Navigate into the project directory:
```bash
cd chat_app1
```
3. Install the required dependencies using pip:
```bash
pip install -r requirements.txt
```
4. Create a new virtual environment using the following command:
```bash
python -m venv venv
```
5. Activate the virtual environment using the following command:
```bash
source venv/bin/activate
```
6. Configure the environment variables in the `config/settings.py` file:
```python
# config/settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```
7. Run the database migrations using the following command:
```bash
python manage.py migrate
```
8. Run the development server using the following command:
```bash
python manage.py runserver
```
9. Open a web browser and navigate to `http://localhost:8000` to access the chat application.

Note: This project uses Django Channels, which requires a Redis server to be running in the background. You can install Redis using your package manager or by following the instructions on the official Redis website.