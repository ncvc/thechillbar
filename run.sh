#!/bin/bash
# Run server - accessible from the outside

echo 'Starting server'
python manage.py runserver 0.0.0.0:8000

