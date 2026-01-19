# code-quest
A Django-based scalable backend system using Celery, Redis, and NGINX for asynchronous task handling, caching, and production-ready server deployment.


CodeQuest is a Django-based backend platform designed with a production-level architecture, integrating Celery, Redis, and NGINX to handle asynchronous tasks, background processing, and scalable server deployment.

This project is aimed at understanding real-world backend workflows, including task queues, caching, reverse proxy servers, and distributed systems.

<img width="452" height="245" alt="image" src="https://github.com/user-attachments/assets/292c95af-e31b-4ff7-9c4b-b727913c51bc" />



Tech Stack
Backend Framework: Django
Task Queue: Celery
Message Broker & Cache: Redis (Memurai)
Web Server / Control Engine: NGINX
Production Server: Waitress
Tunnel / Public Hosting: Ngrok

External Dependencies (Manual Downloads)
Download and install the following before running the project:
Memurai.exe (Redis for Windows)
Redis Insight
NGINX

Python Dependencies
Install all required Python packages using CMD:
pip install Django
pip install celery
pip install django-redis
pip install django-celery-results
pip install redis
pip install waitress
pip install whitenoise

Finding Your IP Address
To find your IPv4 address:
ipconfig

Database Migrations
Navigate to the project directory:
cd C:\Users\[USERNAME]\Downloads\code-quest\code-quest\


Run migrations:
python manage.py makemigrations
python manage.py migrate

Running Core Services
Start Redis (Memurai)
cd "C:\Program Files\Memurai"
memurai.exe

Start Celery Worker
cd C:\Users\[USERNAME]\Downloads\code-quest\code-quest\
celery -A sixteen worker --pool=solo -l info

Start NGINX
cd C:\Users\[USERNAME]\Downloads\nginx-1.27.2\nginx-1.27.2
start nginx

Important Note
Celery, Redis, and NGINX must be running before starting the Django server.

Running the Django Server
Localhost (only your device)
python manage.py runserver

Same Network (other laptops on same IP)
python manage.py runserver <your-ip>:8000

Recommended (Production-style)
cd C:\Users\[USERNAME]\Downloads\code-quest\
python run_waitress.py

Making the Server Public (Online Access)
Visit: https://dashboard.ngrok.com/get-started/your-authtoken
Add your Ngrok auth token as instructed
Expose the local server using Ngrok
