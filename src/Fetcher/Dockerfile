# Use the official Python image from the Docker Hub
FROM python:3.9.20-alpine3.20

COPY . /app

# Set the working directory to /app
WORKDIR /app

# Install the required packages
COPY requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r /requirements.txt

# Expose the port the app runs on
EXPOSE 8000

# We will run this app like this, to run 2 programs in the container:
# * 1 for scanning the database, and watching changes there or something
# * the other, for running fastapi for fetching images from the internet as needed
CMD ["sh", "/app/main.sh"]