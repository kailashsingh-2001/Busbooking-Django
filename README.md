# BusBook – Bus Ticket Booking System

A Django web app to search buses, choose seats and book tickets.

## Features
- Search buses by route and date
- Live seat availability and seat selection
- Sign up / login
- Database constraint that prevents double-booking
- Customised Django admin

## Tech stack
Python, Django, SQLite, HTML, CSS, JavaScript

## Run locally
    git clone  https://github.com/kailashsingh-2001/Busbooking-Django.git
    cd busbooking
    python -m venv venv
    venv\Scripts\Activate.ps1
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed_buses
    python manage.py createsuperuser
    python manage.py runserver

## Screenshots
![alt text](image.png)![alt text](image-1.png)![alt text](image-2.png)