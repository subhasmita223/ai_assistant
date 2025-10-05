# Use Python 3.12 base image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for pygame and audio
RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    libjpeg-dev \
    python3-dev \
    python3-numpy \
    libespeak-dev \
    espeak \
    alsa-utils \
    pulseaudio \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create assets directory if it doesn't exist
RUN mkdir -p assets

# Set environment variables
ENV DISPLAY=:0
ENV PULSE_RUNTIME_PATH=/var/run/pulse

# Expose port (if needed for web interface in future)
EXPOSE 8080

# Create a non-root user for security
RUN useradd -m -u 1000 therapist && \
    chown -R therapist:therapist /app
USER therapist

# Command to run the application
CMD ["python", "main.py"]