# Dockerfile
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies first (for build tools and libraries)
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements.txt to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies with retry and timeout
RUN pip install --timeout=100 --resume-retries=5 -r requirements.txt

# Remove build dependencies to reduce image size
RUN apt-get purge -y --auto-remove gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Use exec form for CMD
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
