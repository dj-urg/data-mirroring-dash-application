# Use the official Python base image
FROM python:3.9-slim

# Create a non-root user and switch to it
RUN useradd -ms /bin/bash appuser
USER appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install the dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY --chown=appuser:appuser .env .

# Expose the port the app runs on
EXPOSE 8051

# Command to run the application using Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8051", "wsgi:app"]