# Use slim Python base image
FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        awscli \
        ffmpeg \
        libsm6 \
        libxext6 \
        unzip \
        gcc \
        g++ \
        && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python3", "app.py"]
