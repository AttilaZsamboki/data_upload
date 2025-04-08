#!/bin/bash


# Set environment variables properly
export PYTHONPATH=/app
export PATH=/usr/local/bin:$PATH

# Load environment variables from Docker runtime (not build-time)
cd /app

source envs.env

export GOOGLE_CREDENTIALS=$GOOGLE_CREDENTIALS
export DB_HOST=$DB_HOST
export DB_NAME=$DB_NAME
export DB_PASS=$DB_PASS
export DB_PORT=$DB_PORT
export DB_USER=$DB_USER

printenv > /app/envs.log

# Function to run Django command
# Check if argument is provided
if [ -z "$1" ]; then
    echo "Error: Command argument is required"
    exit 1
fi

# Execute the specified function
python3 "$1"
