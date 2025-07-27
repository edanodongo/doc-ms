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

# Install Python dependencies
RUN pip install -r requirements.txt

# Remove build dependencies to reduce image size
RUN apt-get purge -y --auto-remove gcc libpq-dev && \
	rm -rf /var/lib/apt/lists/*


# Copy project files
COPY . /app/

# Expose port 8000
EXPOSE 8000

# Use exec form for CMD
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



# # Dockerfile
# FROM python:3.10-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # Set work directory
# WORKDIR /app

# # Install dependencies
# COPY requirements.txt /app/
# RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends gcc libpq-dev \
# 	&& pip install --upgrade pip && pip install -r requirements.txt \
# 	&& apt-get purge -y --auto-remove gcc libpq-dev \
# 	&& rm -rf /var/lib/apt/lists/*

# # Copy project files
# COPY . /app/

# # Expose port 8000
# EXPOSE 8000

# # Default command
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
