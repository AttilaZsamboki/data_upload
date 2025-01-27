FROM python:3.11.4

WORKDIR /app

ARG DB_HOST
ARG DB_NAME
ARG DB_PASS
ARG DB_PORT
ARG DB_USER

ENV DB_HOST=${DB_HOST}
ENV DB_NAME=${DB_NAME}
ENV DB_PASS=${DB_PASS}
ENV DB_PORT=${DB_PORT}
ENV DB_USER=${DB_USER}

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/dataupload/media/upload_files
RUN mkdir -p /app/dataupload/media/files
RUN mkdir -p /app/files
RUN apt-get update && apt-get install -y cron dos2unix

COPY . /app/
RUN dos2unix /app/manage.py
RUN dos2unix /app/docker-entrypoint.sh
RUN dos2unix /app/crontab.sh
RUN chmod +x /app/manage.py /app/docker-entrypoint.sh /app/crontab.sh

RUN echo "SHELL=/bin/bash" > /etc/cron.d/app-cron
RUN echo "BASH_ENV=/app/env.sh" >> /etc/cron.d/app-cron

# Set up crontab
RUN echo '*/10 * * * * /app/crontab.sh upload_file' >> /etc/cron.d/app-cron
RUN echo '*/5 * * * * /app/crontab.sh upload_feed_daily' >> /etc/cron.d/app-cron
RUN echo '30 * * * * /app/crontab.sh upload_feed_hourly' >> /etc/cron.d/app-cron
RUN echo '0 1 * * 5 /app/crontab.sh upload_feed_weekly' >> /etc/cron.d/app-cron
RUN echo '0 0 * * * /app/crontab.sh fol_orders_delete_last_90' >> /etc/cron.d/app-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/app-cron

# Apply cron job
RUN crontab /etc/cron.d/app-cron

EXPOSE 8001
ENTRYPOINT ["./docker-entrypoint.sh"]
CMD ["daphne", "-b", "0.0.0.0", "-p", "8001", "dataupload.asgi:application"]
