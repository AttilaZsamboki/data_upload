#!/bin/bash

source /app/envs.log

# Set environment variables
export DJANGO_SETTINGS_MODULE=dataupload.settings
export PYTHONPATH=/app
export PATH=/usr/local/bin:$PATH

# Change to app directory
cd /app

# Function to run Django command
run_django_command() {
    /usr/local/bin/python << EOF
import django
django.setup()
from api.cron import $1
$1()
EOF
}

# Check if argument is provided
if [ -z "$1" ]; then
    echo "Error: Command argument is required"
    exit 1
fi

# Execute the specified function
case "$1" in
    "upload_file"|"upload_feed_daily"|"upload_feed_hourly"|"upload_feed_weekly"|"fol_orders_delete_last_90"|"health_check")
        run_django_command "$1"
        ;;
    *)
        echo "Unknown command: $1"
        exit 1
        ;;
esac
