# Use slim Python base image
FROM python:3.12-slim

# Install system dependencies required by OpenCV
RUN apt-get update && apt-get install -y \
  libgl1-mesa-glx \
  libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into container
COPY . .

# Expose port for the web server
EXPOSE 8080

# Start the app using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "main:app"]

