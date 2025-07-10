# Base image: Python 3.12 (slim to keep it lightweight)
FROM python:3.12-slim

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy all project files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your Flask app runs on
EXPOSE 8080

# Command to run your Flask app with Gunicorn (better for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]
