# Use the official Python image from the Docker Hub
FROM python:3.9.20-alpine3.20

# Install the required packages
COPY REST_API/requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

COPY REST_API /app

COPY ORMSchema /app/ORMSchema
COPY .env /app/.env
# Set the working directory to /app
WORKDIR /app

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0"]
