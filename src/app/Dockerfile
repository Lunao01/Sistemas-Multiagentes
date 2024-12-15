# Use the official Python image from the Docker Hub
FROM python:3.9.20-alpine3.20

# Install the required packages
COPY app/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# Copy all files and directories from the current directory
COPY  app /app 

COPY ORMSchema /app/ORMSchema
COPY .env /app/.env

# Set the working directory to /app
WORKDIR /app

# Expose the port the app runs on
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
