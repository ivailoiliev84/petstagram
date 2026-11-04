#!/bin/bash

echo "stopping petstagram system"

# --------- Stop Gunicorn ----------
PID_FILE="gunicorn.pid"

if [ -f "$PID_FILE" ]; then
    PID=$(cat "$PID_FILE")

    if kill -0 "$PID" 2>/dev/null; then
        kill -TERM "$PID"
        echo "Gunicorn stopped (PID $PID)."
    else
        echo "Gunicorn not running, removing stale PID file."
    fi

    rm -f "$PID_FILE"
else
    echo "Gunicorn is not running."
fi
