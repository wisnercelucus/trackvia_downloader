# Set the default port
ARG PORT=443

# Use the Cypress browsers image as the base
FROM cypress/browsers:latest

# Install Python and required tools
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv && \
    apt-get clean

# Set environment variables for the virtual environment
ENV VIRTUAL_ENV=/app/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV

# Copy the requirements file
COPY requirements.txt /app/requirements.txt

# Set the working directory
WORKDIR /app

# Install dependencies in the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files
COPY . /app

# Expose the port and set the default command
EXPOSE $PORT
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "${PORT}"]