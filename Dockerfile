# Base image
FROM python:3.11-slim

# Install required dependencies, including Chromium and the correct ChromeDriver
RUN apt-get update && apt-get install -y \
    wget curl unzip chromium chromium-driver && \
    apt-get clean

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PATH="/usr/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app

# Expose the application port
EXPOSE 3000

# Run the application using Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:3000", "app:app"]
