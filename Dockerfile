# Use slim Python base image
FROM python:3.8-slim-buster

# Set working directory
WORKDIR /app

# Prevent Python from buffering stdout/stderr (helps logs)
ENV PYTHONUNBUFFERED=1

# Install system dependencies (kept same as your original + apt-clean)
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

# Copy only requirements first to leverage Docker layer caching
COPY requirements.txt /app/requirements.txt

# Upgrade pip and install python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Now copy the rest of the application
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Use Streamlit as the process (runs headless and binds to 0.0.0.0)
# --server.enableCORS=false helps when you access from different host (optional)
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--server.headless=true", "--server.enableCORS=false"]
