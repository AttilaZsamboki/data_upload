#!/bin/bash


# Set environment variables properly
export PYTHONPATH=/app
export PATH=/usr/local/bin:$PATH

# Load environment variables from Docker runtime (not build-time)
cd /app

source envs.env

export GOOGLE_CREDENTIALS=$GOOGLE_CREDENTIALS

printenv > /app/envs.log

# Function to run Django command
# Check if argument is provided
if [ -z "$1" ]; then
    echo "Error: Command argument is required"
    exit 1
fi

# Execute the specified function
"$1"
