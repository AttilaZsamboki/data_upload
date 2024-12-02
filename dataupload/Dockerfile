FROM python:3.11.4

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/
ENV PYTHONPATH=/app
EXPOSE 8001
