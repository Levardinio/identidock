#!/bin/sh
set -e

if [ "$ENV" = 'DEV' ]; then
    echo "Running Development Server"
    exec python /app/identidock.py
else
    echo "Running Production Server"
    exec uwsgi --http 0.0.0.0:5000 --wsgi-file /app/identidock.py \
               --callable app --stats 0.0.0.0:9191
fi
