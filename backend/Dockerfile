FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create data directory if it doesn't exist
RUN mkdir -p data

# Expose the port FastAPI will run on
EXPOSE 7860

# Run the application
CMD ["python", "app.py"]
