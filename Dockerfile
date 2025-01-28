# Set the default port
ARG PORT=443

# Use the Cypress browsers image as the base
FROM cypress/browsers:latest

# Install Python 3 and required tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean

# Set environment variables for Python packages
ENV PATH=/root/.local/bin:${PATH}

# Copy the requirements file to the container
COPY requirements.txt /app/requirements.txt

# Set the working directory
WORKDIR /app

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy all project files to the container
COPY . /app

# Set the default command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]