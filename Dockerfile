# syntax=docker/dockerfile:1

# Use an official Python image as a base
FROM python:3.12.5-bookworm

# Set the working directory to /contrans2024
WORKDIR /contrans2024

# Copy the requirements file into the working directory
COPY requirements.txt requirements.txt

# Install the dependencies using pip
RUN pip install --upgrade pip && pip install -r requirements.txt
RUN python -m nltk.downloader stopwords punkt wordnet

# Expose the port for the dashboard
EXPOSE 8050

# Run the dashboard when the container launches
CMD ["python", "app.py"]