#!/bin/bash

set -e

# Move to project directory
cd "$(dirname "$0")"

echo "Starting Petstagram system..."

# Check if Gunicorn is already running
PID_FILE="gunicorn.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        echo "Gunicorn is already running (PID $PID)."
        exit 1
    fi

    echo "Removing stale PID file."
    rm -f "$PID_FILE"
fi

# Load environment variables
set -a
source ./.env
set +a

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt --quiet

# Django setup
python manage.py migrate
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn core.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --timeout 120 \
    --daemon \
    --pid "$PID_FILE"

echo "Gunicorn started."
echo "Petstagram system started successfully."
