FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install curl
RUN apt-get update && apt-get install -y curl

# Copy requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install -r requirements.txt

# Cron jobs configuration
RUN apt-get update && apt-get install -y cron

COPY cronjobs /etc/cron.d/cronjobs

RUN chmod 0644 /etc/cron.d/cronjobs

# Copy application files
COPY app app

# Expose port
EXPOSE 80

# Start application with Uvicorn
CMD cron && uvicorn app:app --host 0.0.0.0 --port 80

