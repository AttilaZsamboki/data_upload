#!/bin/bash


# Set environment variables properly
export DJANGO_SETTINGS_MODULE=dataupload.settings
export PYTHONPATH=/app
export PATH=/usr/local/bin:$PATH

# Load environment variables from Docker runtime (not build-time)
cd /app

source envs.env

export DB_HOST=$DB_HOST
export DB_NAME=$DB_NAME
export DB_PASS=$DB_PASS
export DB_PORT=$DB_PORT
export DB_USER=$DB_USER

printenv > /app/envs.log

# Function to run Django command
run_django_command() {
    /usr/local/bin/python << EOF
import django
import dotenv
dotenv.load_dotenv()

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
