#!/bin/bash
# Run server - accessible from the outside

echo 'Starting server'
sudo python manage.py runserver 0.0.0.0:80
