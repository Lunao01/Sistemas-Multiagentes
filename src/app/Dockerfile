# Use the official Python image from the Docker Hub
FROM python:3.9.20-alpine3.20

# Copy all files and directories from the current directory
COPY . /app 

COPY ../ORMSchema /app/ORMSchema
COPY ../.env /app/.env

# Set the working directory to /app
WORKDIR /app

# Install the required packages
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["flask", "run", "--host", "0.0.0.0", "--port", "8000"]
