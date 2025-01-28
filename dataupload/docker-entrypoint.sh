#!/bin/sh
# docker-entrypoint.sh

# If this is going to be a cron container, start cron in foreground
if [ "$1" = cron ]; then
    # Create log file if it doesn't exist
    touch /app/logs/cron.log
    
    # Start cron in foreground mode
    cron -f
else
    exec "$@"
fi
