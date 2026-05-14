# Hugging Face Spaces requires the container to listen on port 7860.
# This Dockerfile is identical to the original Render one except for the port
# and the non-root user (HF convention).
FROM python:3.11-slim

# HF Spaces convention: run as a non-root user with uid 1000
RUN useradd -m -u 1000 user

WORKDIR /app

# Install Python dependencies first for better layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code with correct ownership
COPY --chown=user . /app

# Make the startup script executable
RUN chmod +x start.sh

# Switch to the non-root user before running
USER user

# HF Spaces port (was 5000 on Render)
EXPOSE 7860

CMD ["bash", "start.sh"]
