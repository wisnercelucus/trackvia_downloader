# Base image
FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    wget curl chromium-driver && \
    apt-get clean

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install Python packages
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install additional dependencies
RUN pip install gunicorn flask selenium webdriver-manager

# Expose port
EXPOSE 3000

# Command to run the app
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
