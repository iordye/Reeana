# Dockerfile

# Use official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Health checks
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests,sys; \
  sys.exit(0 if requests.get('http://localhost:8000/health').status_code==200 else 1)"

# Start the application
CMD ["uvicorn", "reeana.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
