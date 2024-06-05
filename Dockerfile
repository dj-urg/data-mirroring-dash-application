# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8051 available to the world outside this container
EXPOSE 8051

# Define environment variable
ENV NAME World

# Run wsgi.py when the container launches
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8051", "wsgi:app"]
