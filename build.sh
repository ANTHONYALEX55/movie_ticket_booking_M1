#!/bin/bash
set -e

cd /home/ubuntu/movie_ticket_booking_M1

git pull origin main

source venv/bin/activate

pip install -r requirements.txt

python manage.py migrate --noinput

python manage.py collectstatic --noinput

sudo systemctl restart django_app

echo "Deployment completed successfully!"
