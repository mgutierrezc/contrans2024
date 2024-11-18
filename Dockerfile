# syntax=docker/dockerfile:1

# Use the official Debian Bookworm image as the base image
FROM python:3.12.5-bookworm

# Set the working directory
WORKDIR /contrans2024

# Copy the current directory contents into the container at /app
COPY requirements.txt requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Make port 8888 available to the world outside this container
EXPOSE 8050

# Run app.py when the container launches
CMD ["python", "app.py"]