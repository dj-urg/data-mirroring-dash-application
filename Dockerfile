# Use a smaller base image to minimize the attack surface
FROM python:3.9-slim

# Create a non-root user and switch to it
RUN useradd -ms /bin/bash appuser
USER appuser

# Set the working directory in the container
WORKDIR /app

# Add the local user pip directory to the PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Install security updates and necessary packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements.txt file and install the dependencies
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY --chown=appuser:appuser . .

# Expose the port the app runs on
EXPOSE 8051

# Command to run the application using Gunicorn
CMD ["gunicorn", "--workers", "3", "--timeout", "120", "--bind", "0.0.0.0:8051", "main:application"]
