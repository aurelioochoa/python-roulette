FROM python:3.11-slim

# Disable bytecode generation (__pycache__ directories)
ENV PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies for audio/SDL
RUN apt-get update && apt-get install -y \
    libsdl2-mixer-2.0-0 \
    libsdl2-2.0-0 \
    pulseaudio-utils \
    && rm -rf /var/lib/apt/lists/*

# Copy project into working directory
COPY . .

# Set working directory for source files directory
WORKDIR /app/source

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the game
CMD ["python3", "game.py"]