FROM python:3.11.4

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir -p /app/dataupload/media/upload_files

COPY . /app/
EXPOSE 8001
