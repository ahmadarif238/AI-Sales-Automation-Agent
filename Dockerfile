# Root Dockerfile for Hugging Face Spaces
FROM python:3.11-slim

WORKDIR /app

# Copy the backend requirements first
COPY backend/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r ./requirements.txt

# Copy all backend code from the backend/ directory to /app
COPY backend/ .

# Ensure data directory exists
RUN mkdir -p data

# Hugging Face Spaces uses port 7860
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
